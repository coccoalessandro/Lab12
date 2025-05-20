from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():

    @staticmethod
    def getCountries():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary = True)

        result = []

        query = """select distinct(Country)
                    from go_retailers"""
        cursor.execute(query)

        for row in cursor:
            result.append(row['Country'])

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getRetailers(country):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select *
                    from go_retailers g
                    where g.Country = %s"""

        cursor.execute(query, (country,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getEdges(year, country, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select gds1.Retailer_code r1, gds2.Retailer_code r2, count(distinct(gds1.Product_number)) as n
                    from go_daily_sales gds1, go_daily_sales gds2, go_retailers g1, go_retailers g2
                    where year(gds1.`Date`) = year(gds2.`Date`)
                    and year(gds1.`Date`) = %s
                    and gds1.Product_number = gds2.Product_number
                    and gds1.Retailer_code < gds2.Retailer_code
                    and gds1.Retailer_code = g1.Retailer_code and gds2.Retailer_code = g2.Retailer_code
                    and g1.Country = %s
                    and g2.Country = %s
                    group by gds1.Retailer_code, gds2.Retailer_code"""

        cursor.execute(query, (year, country, country,))

        for row in cursor:
            result.append((idMap[row['r1']], idMap[row['r2']], row['n']))

        cursor.close()
        conn.close()

        return result


