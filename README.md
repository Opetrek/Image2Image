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

