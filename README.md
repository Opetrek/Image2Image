# Генерация изображений на основе скетчей

## Описание проекта
Здесь представлен проект, который позволяет преобразовывать скетчи в цветные изображения с использованием нейросети Stable Diffusion.

## Возможности
- Преобразование черно-белых изображений в цветные с высоким качеством
- Легкий доступ к функционалу через платформу Stability Matrix
- Доступ к различным параметрам и настройкам внутри кода для получения оптимальных результатов

## Требования к системе
- Установленный Stability Matrix
- Совместимость с операционными системами: Windows 10/11, Linux, Mac OS
- Видеокарты от Nvidia 30 серии
- Оперативная память: от 8 до 16 ГБ
- Свободное место на диске: до 20 ГБ

## Установка и запуск
Перейдите по ссылке [Stability Matrix](https://github.com/LykosAI/StabilityMatrix) и устанавливаем платформу в соответствии с вашей операционной системой.

![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20SM.png)

Установку Stability Matrix рекомендуется проводить по умолчанию, без всяких изменений в расположении файла.
После установки, открыть Stability Matrix и откроется вкладка с такой моделью: 

![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/Установка%20Stable%20Duffision%20ч.1.png)

Необходимо дальше добавить необходимую модель, внизу находится кнопка "Add package"/ "Добавить пакет". Для дальнейшей работы необходимо установить Stable Diffusion WebUI от Automatic 1111.

![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/Установка%20SD%202.1.png)


## Руководство по Stable Diffusion

После установки Stable Diffusion, открываем его через Stability Matrix, и откроется главное окно:

![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/Настройка%20SD%20ч1.png)

Изначально блок ControlNet будет отсутствовать в установленной программе. Для её установки требуется перейти во вкладку "Extensions" и перейти на "Install to URL"

![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/Настройка%20SD%20ч2.png)

Ссылка из скриншота выше [ControlNet](https://github.com/Mikubill/sd-webui-controlnet)

Подставьте ссылку и нажмите Install. Процесс установки займёт некоторое время, после этого рекомендуется перезапустить Stable Diffusion.

После этого у вас появится блок ControlNet, но будут отсутствовать модели для него.

![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/Настройка%20SD%20ч3.png)

Для установки необходимых моделей необходимо перейти по ссылке:  [модели ControlNet](https://github.com/Mikubill/sd-webui-controlnet/wiki/Model-download)
Там будет описано установка ControlNet и выбор моделей

![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/Настройка%20SD%20ч4.png)

На ваше усмотрение, выбирайте по весу модель ControlNet. В рамках данного проекта было выбрано модель с весами "Large".
Выбрав любую ссылку из предложенных, вы перейдете на Hugging Face на страницу с предложенными моделями, разного типа.

![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/Настройка%20SD%20ч5.png)

Названия модели связаны с ControlNet в разделе ControlType.

![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/Настройка%20SD%20ч6.png)

Для первого раза рекомендуется установить модели Canny, Lineart, Depth с pth-файлами. Для ознакомления с типами ControlNet можете самостоятельно поискать в интернете или перейти на [обзор](https://www.itshneg.com/controlnet-upravlyaj-pozami-v-stable-diffusion/) для ознакомления.

После скачивания, необходимо модели перетащить в папку ControlNet для работы. Путь к файлу показан ниже, при установке Stability Matrix по умолчанию.

![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/Настройка%20SD%20ч7.png)

После переноса файлов рекомендуется перезапустить Stable Diffusion, и у вас появятся модели с ControlNet.

## Руководство по запуску Stable Diffusion с помощью API

Дальше будем предварительно запускать части кода, который представляет собой поэтапное развёртывание нашего проекта.

### Предварительный запуск Stable Diffusion.
Для запуска необходимо импортировать библиотеки webuiapi и pillow.
```
import webuiapi
from PIL import Image

# create API client
api = webuiapi.WebUIApi()

# create API client with custom host, port
api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)

options = {'sd_model_checkpoint': '0001softrealistic_v187xxx.safetensors [877aac4a95]'}
api.set_options(options)

image_path = r"C:\Users\fidan\OneDrive\Рабочий стол\imag\3.jpg"
raw_image=Image.open(image_path).convert('RGB')

img = raw_image

unit1 = webuiapi.ControlNetUnit(input_image=img, module='canny', model='control_v11p_sd15_canny [d14c016b]', weight=0.3)
unit2 = webuiapi.ControlNetUnit(input_image=img, module='lineart_standard', model='control_v11p_sd15_lineart [43d4be0d]', weight=0.7)

r2 = api.img2img(prompt="beatiful girl",
            images=[img],
            width=512,
            height=512,
            controlnet_units=[unit1, unit2],
            sampler_name="Euler a",
            cfg_scale=7,
           )

fidan=r2.image
fidan.save('fidan.png')
```
Что подавалось на вход в текущем примере
![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/Запуск%20SD%20дистанционно%20ч1.jpg)

И что сгенерировал Stable Diffusion

![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/Запуск%20SD%20дистанц%20ч2.png)

### Предварительный запуск BLIP и ChatGPT.
Теперь используем следующий код для получения описания картинки, использующий модель BLIP и ChatGPT( версия 3.5). Для запуска программы рекомендуются установить библиотеки requests, transformers, g4f 
и pillow с предыдущего примера.

```
import requests

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from g4f.client import Client

processor = BlipProcessor.from_pretrained("unography/blip-long-cap")
model = BlipForConditionalGeneration.from_pretrained("unography/blip-long-cap")

image_path=r"C:\Users\fidan\OneDrive\Рабочий стол\imag\3.jpg"
raw_image=Image.open(image_path).convert('RGB')

text = "A photography of"
inputs = processor(raw_image, text, return_tensors="pt")
out = model.generate(**inputs)
caption = processor.decode(out[0], skip_special_tokens=True)
#print(caption)

client = Client()
a = ("сократи текст выделив основные детали, которые требуются, чтобы раскрасить рисунок. Текст будет использоваться как промпт. Ответ дай на английском языке, так же через запятую"
     "текст:")
v = ("Помоги мне написать промпт по правилам ниже. Ты создаешь промпт для обработки изображения. В тексте могут встречаться упоминания того что изображение нарисовано карандашом - убери или замени это на реалистичный стиль, чтобы выглядело как фотография."
     "Правила:"
     "1) промпт состоит из отдельных слов или коротких словосочетаний перечисляемых через запятую на английском языке"
     "2) в промпте не должно быть упоминания любых стилей кроме реалистичного. "
     "3) промпт должен содержать описание для разукрашивания того, что на изображении"
     "В ответе напиши мне только промпт для  ")

c = a + " " + caption
#print(c)

def gpt(c):
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": c}],
        )
    d = response.choices[0].message.content
    return d
# сокращение
z = gpt(c)
z1 = v + " " + z
t = gpt(z1)
print(t)
```

На выводе получаем: "person, glasses, scarf, neck, wearing".


Теперь есть описание картинки и возможность её обработать. Осталось лишь соединить их для совместной работы, и так же представить сам код в каком-нибудь сервисе - в рамках проекта был выбран телеграмм бот,
т.к. он прост и удобен. 

 В данном случае просто рассмотрим уже готовый код с телеграмм ботом и посмотрим результаты.

## Запуск telegram-bot с моделью Blip, ChatGPT и Stable Diffusion.

```
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
```

Результат работы 
![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/Результат%20работы%20бота%20ч1.png)

![Пример результата модели](https://github.com/Opetrek/Image2Image/blob/main/screens/Результат%20работы%20бота%20ч2.png)

