import telebot
import requests
import webuiapi

from telebot import types
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from g4f.client import Client

# TOKEN="5995667124:AAFoRVCAdEmdTX-3a8i5uLT7Lqj42_C_phw"
# bot = telebot.TeleBot('5995667124:AAFoRVCAdEmdTX-3a8i5uLT7Lqj42_C_phw')

TOKEN = "6691027735:AAHlJ6T4S9Hyzj862MKDbK3P_ckM-0JW-IA"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помощник! Нажми 'Начать', чтобы приступить.",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Начать':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Строго по скетчу')
        btn2 = types.KeyboardButton('Улучшить скетч')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, '❓ Выберите интересующий вас вариант', reply_markup=markup)

    elif message.text in ['Строго по скетчу', 'Улучшить скетч']:
        mode = 'canny' if message.text == 'Строго по скетчу' else 'depth_anything'
        model = 'control_v11p_sd15_canny [d14c016b]' if message.text == 'Строго по скетчу' else 'control_v11f1p_sd15_depth [cfd03158]'
        weights = (0.3, 0.7) if message.text == 'Строго по скетчу' else (0.4, 0.6)

        bot.send_message(message.from_user.id, "📸 Пришлите ваше фото для обработки.")
        bot.register_next_step_handler(message, process_photo, *weights, mode, model)


def process_photo(message, a, b, c, d):
    if message.content_type == 'photo':
        photo_data = message.photo[-1]
        file_id = photo_data.file_id
        file_path = bot.get_file(file_id)
        photo_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path.file_path}"

        processor = BlipProcessor.from_pretrained("unography/blip-long-cap")
        model = BlipForConditionalGeneration.from_pretrained("unography/blip-long-cap")
        raw_image = Image.open(requests.get(photo_url, stream=True).raw).convert('RGB')
        text = "a photography of"
        inputs = processor(raw_image, text, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        """
        client = Client()
        prompt_request = (
            "Помоги мне написать промпт по правилам ниже. Ты создаешь промпт для обработки изображения. В тексте могут "
            "встречаться упоминания того что изображение нарисовано карандашом - убери или замени это на реалистичный стиль, "
            "чтобы выглядело как фотография. "
            "Правила: "
            "1) промпт состоит из отдельных слов или коротких словосочетаний перечисляемых через запятую на английском языке "
            "2) в промпте не должно быть упоминания любых стилей кроме реалистичного. "
            "3) промпт должен содержать описание для разукрашивания того, что на изображении. "
            "В ответе напиши мне только промпт."
        )

        prompt = prompt_request + caption

        def gpt(prompt):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

        detailed_prompt = gpt(prompt)
        additional_prompt = "contrast, colorful, photorealistic image, high detalization, clarity, blurred background, 4k, realistic proportions, natural proportions, beautiful body and face, smooth the drawn lines, remove extra lines"
        final_prompt = additional_prompt + ' ' + detailed_prompt
        print(final_prompt)
        """

        final_prompt = caption
        api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)
        options = {'sd_model_checkpoint': '0001softrealistic_v187xxx.safetensors [877aac4a95]'}
        api.set_options(options)

        image = raw_image
        unit1 = webuiapi.ControlNetUnit(input_image=image, module=c, model=d, weight=a)
        unit2 = webuiapi.ControlNetUnit(input_image=image, module='lineart_standard',
                                        model='control_v11p_sd15_lineart [43d4be0d]', weight=b)

        result = api.img2img(
            prompt=final_prompt,
            negative_prompt="Unrealistic styles, cartoon, anime, black and white, non-contrast, ugly face, ugly body shape, anatomical errors, disproportionate body parts, pale colors, not according to image, effects that may make the image blurry or unrealistic, ugly eyes, unreal eyes",
            images=[image],
            width=512,
            height=512,
            controlnet_units=[unit1, unit2],
            sampler_name="Euler a",
            cfg_scale=7,
        )
        generated_image = result.image
        generated_image.save('generated_image.png')

        with open('generated_image.png', 'rb') as img:
            bot.send_photo(message.from_user.id, img, caption="Ваше сгенерированное изображение")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Строго по скетчу')
        btn2 = types.KeyboardButton('Улучшить скетч')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, '❓ Выберите интересующий вас вариант', reply_markup=markup)


bot.polling(none_stop=True, interval=0)
