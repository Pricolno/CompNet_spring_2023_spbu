# Практика 2. Rest Service (сдать до 02.03.2023) 

## 1. Программирование. Rest Service. Часть I 

* Нужно реализовать `GET`, `POST`, `PUT`, `DELETE` для товара `[/web_server]` (3 балла)
* Продемострировать с помощью `Postman` (3 балла)
* Добавить иконки к продуктам без визуализации (4 балла)

### API 
* `host = http://127.0.0.1:5000`
* `/products GET` - попросить список всех товаров
* `/products/<int:product_id> GET` - попросить  товар с `id=product_id`
* `/products/<int:product_id> POST` - добавить товар с `id=product_id`
* `/products/<int:product_id> PUT` - изменить товар с `id=product_id`
* `/products/<int:product_id> DELETE` - удалить товар с `id=product_id`

1. all_products
![](./images/1_all_products.png)
2. get_product_by_id
![](./images/2_get_product_by_id.png)
3. add_product_and_show_him
![](./images/3_add_product.png)
![](./images/3_all_product_with_added.png)
4. put_product_and_show_him
![](./images/4_put_product.png)
![](./images/4_all_product.png)
5. delete_product_and_show_all
![](./images/5_delete_product.png)
![](./images/5_delete_and_show_all.png)




