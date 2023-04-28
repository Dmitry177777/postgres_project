/*#secondTestQuery*/ --название запроса
select
 now(), /*@date title=Дата, javaType=java.util.Date*/ -- тут определяется тип и аттрибуты поля
 17843,  --@weight title=Вес, javaType=float
--тут определеяется параметр запроса id с типом INT, строка `123` для использования в SQL редакторе, т.е. только для тестирования и отладки
        /*$id, type=INT {*/123/*}*/
 ;
/*#secondTestQuery end*/