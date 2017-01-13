**Цель проекта MyGtn:**  
* Написать систему учета регистрации тракторов, самоходных машин и прицепов к ним, а также удостоверений трактористов-машинистов.
* Изучить Python, Django и иже с ними

**Техническая информация:**
* Проект находится на ранней стадии разработки.
* Проект использует python 2.7, django 1.6 , Postgresql (остальные зависимости можно посмотреть в REQUIREMENTS).

**Использование:**
* Для начала работы необходимо перейти на главную страницу (по умолчанию http://127.0.0.1:8000/).
* Для просмотра отсутствующих на главной странице реестров/справочников перейдите в админку.

**Текущая функциональность:**  
* отображение данных реестров/справочников пользователю (работает через общие представление и шаблон).
* добвление записей в реестры/справочники (работает через общие представление и шаблон).
* импорт данных в реестры/справочники (работает через общие механизм импорта данных и шаблон).