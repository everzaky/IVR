# ВЕРЗАКОВ ЕФИМ - "ПАШАН"
# Пользовательские сценарии

### Группа: 10МИ1
### Электронная почта: efimverzakov@gmail.com
### VK: https://vk.com/everzakov
 



* Пользовательский сценарий №1 (Добавление новых товаров в базу данных (только для админов))
   
   1. Пользователь нажимает кнопку "Создать новый товар", программа перенаправляет админа из основого меню в меню создания нового товара, создав новый объект.
   2. Пользователь вводит название товара, программа вводит в поле "name" то, что ввёл пользователь, проверив на правильность характеристики данных.
   3. Если существует товар с эти именем, то программа помечает данное поле красным и выводит сообщение: "Товар с эти именем уже существует".
   4. Пользователь загружает фотографию нового товара, программа вводит в поле "image" относительный путь на сервере, изображения которое загрузил пользователь. 
   5. Если у изображения большой размер, т.е. он превышает верхнюю границу возможных размеров, которая в дальнейщем будет определена, то программа помечает данное поле красным и выводит сообщение: "Изображение имеет большой размер, загрузите изображение с размером в пределах до {верхняя граница возможных товаров}".
   6. Пользователь вводит название производителя, программа вводит в поле "producer" то, что ввёл пользователь, проверив на правильность характеристики данных.
   7. Пользователь вводит стоимость товара, программа вводит в поле "price" то, что ввёл пользователь, проверив на правильность характеристики данных.
   8. Пользователь вводит описание товара, программа вводит в поле "description" то, что ввёл пользователь.
   9. Пользователь вводит название категории товаров, в которой будет находиться товар, программа вводит в поле "category" то, что ввёл пользователь.
   10. Если данной категории не существует, то программа предлагает пользователю создать категорию с данным названием.
   11. Пользователь нажимает кнопку "Сохранить новый товар", если никакое поле не помечено красным, то сохраняет новый объект на сервере, иначе переходит к полю, которое помечено красным.
   

* Пользовательский сценарий №2 (Добавление новых магазинов сети "АШАН" в базу данных (только для админов)):
   
   1. Пользователь нажимает кнопку "Создать новый магазин", программа перенаправляет админа из основого меню в меню создания нового магазина, создав новый объект.
   2. Пользователь вводит название магазина, программа вводит в поле "name" то, что ввёл пользователь, проверив на правильность характеристики данных.
   3. Если существует магазин с эти именем, то программа помечает данное поле красным и выводит сообщение: "Магазин с эти именем уже существует".
   4. Пользователь указывает место на карте, где находится данный магазин, программа вводит в поле "location" координаты того места.
   5. Пользователь загружает карту нового магазина, программа вводит в поле "image" относительный путь на сервере изображения, которое загрузил пользователь. 
   6. Если у изображения большой размер, т.е. он превышает верхнюю границу возможных размеров, которая в дальнейщем будет определена, то программа помечает данное поле красным и выводит сообщение: "Изображение имеет большой размер, загрузите изображение с размером в пределах до {верхняя граница возможных товаров}".
   7. Для удобности работы загружается изображение из пункта 6.
   8. Пользователь указывает на карте магазина основные узлы (входы, выходы, пересечения аллей), программа сохраняет их как вершины в графе.
   9. Для удобности вершины высвечиваются на экран.
   10. Пользователь соединяет эти узлы так, что человек бы смог так пройти, программа сохраняет пути между вершины как ребра в графе, расчитывая их длину.
   11. Пользователь создаёт продуктовые аллеи:
       * Пользователь нажимает на кнопку "Создать продуктовуюя аллею", программа создаёт новый объект "alley".
       * Пользователь вводит название продуктовой аллеи, программа вводит в поле "name" то, что ввёл пользователь, проверив на правильность характеристики данных.
       * Пользователь выделяет зоны под аллеи, программа вводит координаты в поле "location" то, что ввёл пользователь.
       * Если новая аллея перекрывает уже созданную, то программа не позваляет это сделать, выводя на экран сообщение:" Данная аллея перекрывает созданную аллею".
       * Пользователь указывает после выделения зоны под аллею узлы и пути, которые находятся возле аллеи, программа вводит в поля "nodes" и "paths" то, что ввёл пользователь, проверив на правильность характеристики данных. 
       * Пользователь заполняет продуктовую аллею, выбирая уже соответсвующие товары, или создаёт новые товары, воспользовавшись пользовательским сценарием №1, программа вводит в поле "products" то, что выбрал пользователь.
       * Пользователь нажимает кнопку "Сохранить продуктовую аллею", программа отправляет объект на сервер, сохраняя в поле "alleys" объекта магазина указатель на аллею.
       * Если пользователю нужно создать ещё аллею, то он снова нажимает на кнопку "Создать продуктовую аллею".
   12. Пользователь нажимает кнопку "Сохранить новый магазин", если никакое поле не помечено красным, то сохраняет новый объект на сервере, иначе переходит к полю, которое помечено красным.
   13. На сервере запускается алгоритм, который будет описан в Пользовательском сценарии № 4.
   
   
* Пользовательский сценарий № 3 (Создание нового списка покупок)

   1. Пользователь нажимает на кнопку "Создать новый список товаров", программа перенаправляет пользователя из основого меню в меню создания нового списка товаров, создав новый объект.
   2. Пользователь нажимает на  кнопку "Ввести новый товар", программа запршаивает данные с помощью json о продуктовых категориях.
   3. Программа обрабатывает полученные данные, предоставляя пользователю выбор продуктовых категорий.
   4. Пользователь выбирает нужную категорию, программа запршивает данные с помощью json о товарах в данной категории.
   5. Пользователь выбирает нужный товар или несколько и нажимает на кнопку "Добавить", программа добавляет выбранные продукты в поле "products".
   6. Пользователь нажимает на кнопку "Вернуться к списку", программа возвращает пользователя к меню создания нового списка товаров.
   7. Если пользователь не нашёл нужный товар, то он нажимает на иконку поиска, и программа ищет данный продукт, если она находит, то показывает найденный продукт пользователю для возможности добавления в список покупок, иначе выводит на экран сообщение: "Данный товар не найден". 
   8. Пользователь выполняет с пункта 4 по поункт 7, если ему нужно добавить новый товар.
   9. Пользователь сохраняет данный список как шаблон, иначе как временный список.
   10. Если пользователь выбрал первый пункт, то он вводит название списка товаров, программа вводит в поле "name" то, что ввёл пользователь, проверив на правильность характеристики данных.
   
  
* Пользовательский сценарий № 4 (Алгоритм для нахождения наименьшего расстояния между вершинами с востанавлением ответа)
   
   \# Скорее всего будет заменён на алгоритм Форда-Беллмана или алгоритм Дейкстры
   
   Алгоритм следующий:
   1. Передаётся номер ячейки.
   2. Создаётся массив расстояний, длина которого равна количеству узлов в магазине.
   3. Ячейка с этим номером равно 0.
   4. Содаётся очередь, в которой будут хранятся номерая ячейек.
   5. Пока очередь не пуста:
      * Берётся номер ячейки с верху очереди.
      * Верхушка очереди удаляется.
      * Для каждой вершины-потомка проверяется: если расстояние от данной вершины + длина ребра между вершинв и вершиной-потомкой меньше расстояния в ячейке вершины-потомка, то обновляется расстоние в ячейке вершины-потомка обновляется, а номер ячйки кладётся в начало очереди и номер родителя вершины-потомка становится равным номеру вершины.
   6. Выходим из алгоритма и возращаем массив расстояний и массив родителей.
     
   Алгоритм выполняется для каждого узла. 
   В поля с номерами объекта передаются то, что возратил алгоритм для каждой вершины.  
   
   
* Пользовательский сценарий № 5  (Основная программа) 

   1. Пользователь нажимает на кнопку "Я в магазине", программа перенаправляет пользователя из основого меню в меню "Я в магазине".
   2. Программа с помощью gps определяет номер магазина.
   3. Получает данные о магазине по его номеру.
   4. Пользователь выбирает список товаров или создаёт новый список, следуя пользовательскому сценарию № 3.
   5. Программа отправляет номер магазина и список товаров на сервер, который обратывает их, используя инструкции в пользовательском сценарии № 6.
   6. Программа получает данные после пункта 4.
   7. Пользователь следует по списку, если он взял продукт, то он отмечает "Я взял продукт", и продукт удаляется из списка.
   8. Если пользователь оттошёл от пути, то он нажимает на кнопку "Вернуться на путь" и выбирает узел по карте, где он находится, программа отправляет список товаров, номер магазина и номер узла, сервер следует инструкциям из пользовтельского сценария №6.
   9. Программа получает данные из пункта №8.
   10. Пользователь следует от пункта 7 до пункта 9.
   11. Когда список пуст, программа выводит сообщение: "Проследуйте до касс".
   


* Пользовательский сценарий № 6 (Упорядочивание товаров в списке)

   1. Подаётся номер магазина, список товаров и первоначальный номер узла.
   2. Программа получает данные о магазине по его номеру.
   3. Если товара нет в магазине, то он удаляется из списка и пользователю сообщается об этом.
   4. Создаётся массив длиной рваной количеству узлов в этом магазине.
   5. Далее ячейки массива заполняются товарами, которые находятся возле данного узла.
   6. Список собирается следующим образом (в начале он находится в первоначальном узле):
      * Возвращает товар, который находится ближе всего к нему.
      * Товар удаляется из ячейки по номеру данного узла.
      * Переходит в этот узел.
   7. Список возвращается также возращается список с товарами в узлах.

* Пользовательский сценарий № 7 (Исследование списков товаров и подключение к другому пользователю)
   
   1. Для каждого пользователя создаётся массив товаров, которые могли бы заинтересовать пользователя.
   2. Он заполняется следующим образом:
       *  Товары, которые пользователь покупает очень много раз.
       *  Товары, которые пользователь покупает по акции отказавшись от обычных товаров.
   3. Также нужно удалять товары из этого списка, еслиЖ
       *  Пользователь не покупал это товар определённое количество раз.
       *  Пользователь не покупает больше этот товар во время акции.
   4. Программа отображает товары из списка в основном меню.

   Возможно, что пользователи смогут вместе ходить по магазинам. Для этого нужно будет придумать          
        

