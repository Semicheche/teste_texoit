from core.db.db import Base
import re

class Movie(object):
    def __init__(self):
        self.buffer = {}

    def get_all(self):
        db = Base()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM movie;")
        val = cursor.fetchall()
        cursor.close()
        return val

    def get_producers_and_years(self):
        db = Base()
        cursor = db.cursor()
        cursor.execute("SELECT `year`, `producer`, `winner` FROM movie;")
        producers = []

        self.buffer['producers'] = {}
        for year, producer, winner in cursor.fetchall():

            producer = producer.replace(' and ', ', ')
            res = re.split(',', producer)

            for r in res:
                if r not in self.buffer['producers'].keys():
                    self.buffer['producers'].setdefault(r, []).append({
                                                                'year': year,
                                                                'winner': 1 if winner else 0})
                else:
                    if year not in[y['year'] for y in self.buffer['producers'][r]]:
                        self.buffer['producers'][r].append({
                                                                'year': year,
                                                                'winner': 1 if winner else 0})

                if 'producer' not in producers:
                    producers.append({
                            'name': r.strip(),
                            'year': year,
                            'win': 1 if winner else 0
                        })
                else:
                    producers.append({
                            'name': r.strip(),
                            'year': year,
                            'win': 1 if winner else 0
                        })
        cursor.close()
        return producers

    def create_interval(self, producers):
        result = []
        for p in producers:
            if p['name'] in self.buffer['producers'].keys():
                for v in self.buffer['producers'][p['name']]:
                    if p['win'] == v['winner']:
                        max_year = v['year'] if p['year'] < v['year'] else p['year']
                        min_year = v['year'] if p['year'] > v['year'] else p['year']
                        interval = (max_year - min_year)
                        if interval:
                            val = {
                                            "producer": p['name'],
                                            "interval": interval,
                                            "previousWin": min_year,
                                            "followingWin": max_year
                                        }
                            if val not in result:
                                result.append(val)

        result.sort(key=lambda x: x['interval'])
        return result

    def get_producer_ordered(self):
        producer_oredered = {}
        final = {'min': [], 'max': []}
        result = self.get_producers_and_years()
        producer_interval = self.create_interval(result)

        for v in producer_interval:
            if v['producer'] in producer_oredered.keys():
                producer_oredered[v['producer']].append(v)

            if v['producer'] not in producer_oredered.keys():
                producer_oredered.setdefault(v['producer'], []).append(v)


        for _, v in producer_oredered.items():
            if len(v) > 1:
                final['min'] += v[:1]
                final['max'] += v[-1:]
        return final