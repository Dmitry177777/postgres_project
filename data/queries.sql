/*#get_companies_and_vacancies_count*/ --получает список всех компаний и количество вакансий у каждой компании

select DISTINCT Employer.employer_name, count(Vacancy.name) as vacancy
from employer Join vacancy USING (id_employer)
GROUP BY Employer.employer_name
 ;
/*#get_companies_and_vacancies_count end*/

/*#get_all_vacancies*/ --получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию

select Employer.employer_name, Vacancy.name,  Vacancy.salary_from, Vacancy.salary_to, Vacancy.salary_currency,Vacancy.response_url
from employer Join vacancy USING (id_employer)
 ;
/*#get_all_vacancies end*/

/*#get_avg_salary*/ --получает среднюю зарплату по вакансиям
select  Vacancy.name, avg(Vacancy.salary_from) as salary_from, avg(Vacancy.salary_to) as salary_to
from vacancy
GROUP BY Vacancy.name
 ;
/*#get_avg_salary end*/

/*#get_vacancies_with_higher_salary*/ --получает список всех вакансий, у которых зарплата выше средней по всем вакансиям

select  Vacancy.name, Employer.employer_name, Vacancy.salary_from, Vacancy.salary_to
from vacancy Join employer USING (id_employer)
Where Vacancy.salary_from > (select avg(salary_from) from vacancy )
 ;
/*#get_vacancies_with_higher_salary end*/

/*#get_vacancies_with_keyword*/ --получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python

select Employer.employer_name, Vacancy.name,  Vacancy.salary_from, Vacancy.salary_to, Vacancy.salary_currency,Vacancy.response_url
from employer Join vacancy USING (id_employer)
WHERE Vacancy.name LIKE '%' || 'разработчик' || '%';
 ;
/*#get_vacancies_with_keyword end*/


