#!/usr/bin/python
# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple
import numpy as np
import math
from copy import deepcopy


class Restaurant:
    def __init__(self, name: str, cost: int, cuisine: str, delivery: int):
        self.name: str = name
        self.cuisine: str = cuisine
        self.delivery: int = delivery
        self.cost: int = cost
        self.style: int = 0
        self.price_ratio: int = 0
        self.max_time: int = 0
        self.atmosphere: int = 0
        self.occasion: int = 0
        self.mark: int = 0

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def get_name(self):
        return self.name

    def get_cuisine(self):
        return self.cuisine

    def get_delivery(self):
        return self.delivery

    def get_cost(self):
        return self.cost

    def get_numerical_parameters(self):
        return self.style, self.price_ratio, self.max_time, self.atmosphere, self.occasion, self.mark

    def set_evaluation(self, marks):
        self.style: int = marks[0]
        self.price_ratio: int = marks[1]
        self.max_time: int = marks[2]
        self.atmosphere: int = marks[3]
        self.occasion: int = marks[4]
        self.mark: int = marks[5]

    def evaluation(self, recommendations):
        lst = np.array([0, 0, 0, 0, 0, 0], dtype='float')
        it = 0
        for restaurant in recommendations:
            if restaurant.get_restaurant_rec() == self.name:
                lst = lst + np.array(restaurant.get_marks(), dtype='float')
                it += 1
        if it != 0:
            lst = lst / it
        self.set_evaluation(lst)

    def get_all_parameters(self):
        return self.name, self.cuisine, self.delivery, self.cost, self.style, self.price_ratio, self.max_time, \
               self.atmosphere, self.occasion, self.mark


class Recommendations:
    def __init__(self, nr: int, restaurant: Restaurant, style: int, price_ratio: int, max_time: int, atmosphere: int,
                 occasion: int, mark: int):
        self.nr: int = nr
        self.restaurant: Restaurant = restaurant
        self.style: int = style
        self.max_time: int = max_time
        self.price_ratio: int = price_ratio
        self.atmosphere: int = atmosphere
        self.occasion: int = occasion
        self.mark: int = mark

    def __eq__(self, other):
        return self.nr == other.nr

    def __hash__(self):
        return hash(self.nr)

    def get_ids(self):
        return self.nr, self.restaurant

    def get_restaurant_rec(self):
        return self.restaurant.get_name()

    def get_marks(self):
        return self.style, self.price_ratio, self.max_time, self.atmosphere, self.occasion, self.mark


class CollaborativeFiltering:  # user-based system!!!
    def __init__(self, rest: List[Restaurant], rec: List[Recommendations]):
        self.restaurants = rest
        self.recommendations = rec
        self.own_recommendations = []

    def add_restaurant(self, restaurant: Restaurant):
        self.restaurants.append(restaurant)

    def get_restaurants(self):
        return self.restaurants

    def add_recommendation(self, nr, restaurant: Restaurant, m_1, m_2, m_3, m_4, m_5, m_6):
        rec = Recommendations(nr, restaurant, m_1, m_2, m_3, m_4, m_5, m_6)
        self.recommendations.append(rec)

    def upload_own_recommendations(self):
        self.own_recommendations = []
        for recommendation in self.recommendations:
            if recommendation.get_ids()[0] == 0:
                self.own_recommendations.append(recommendation)

    def upload_restaurants_marks(self):
        for restaurant in self.restaurants:
            restaurant.evaluation(self.recommendations)

    def get_own_recommendations(self):
        lst = []
        for own in self.own_recommendations:
            lst.append(own.get_ids()[1])
        return lst

    def get_own_rates(self):
        lst = []
        for own in self.own_recommendations:
            record = list(own.get_marks())
            lst.append(record)
        final = np.array(lst, dtype='float')
        return final

    def id_restaurants_amount(self):
        lst = []
        for restaurant in self.restaurants:
            zm = restaurant.get_name()
            if zm not in lst:
                lst.append(zm)
        return lst

    def id_users_amount(self):
        lst = []
        for users in self.recommendations:
            zm = users.get_ids()[0]
            if zm not in lst:
                lst.append(zm)
        lst = sorted(lst)
        return lst

    def user_x_restaurant_matrix(self):
        users = self.id_users_amount()
        restaurants = self.id_restaurants_amount()
        matrix = np.zeros((len(users), len(restaurants)), dtype='float')
        for record in self.recommendations:
            id_user = users.index(record.get_ids()[0])
            id_restaurant = restaurants.index(record.get_ids()[1].get_name())
            matrix[id_user, id_restaurant] = record.get_marks()[5]
        return matrix, users

    def covariance_users_matrix(self) -> List:
        matrix = self.user_x_restaurant_matrix()
        cov_mat = np.corrcoef(matrix[0])
        all_coefficients = cov_mat[0, 1:]
        all_ids = matrix[1][1:]
        zipped = zip(all_ids, all_coefficients)
        dictionary = dict(zipped)
        result = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
        return result

    def get_best_match(self, nr: int):
        result = self.covariance_users_matrix()
        output = []
        if nr < len(result):
            for i in range(nr):
                output.append(result[i][0])
            return output
        else:
            for i in range(len(result)):
                output.append(result[i][0])
            return output  # get only ints - ids (not exact objects)!!!

    def get_best_restaurants(self, nr: int):
        res = self.get_best_match(nr)
        own_rec = self.get_own_recommendations()
        lst = np.zeros((len(res), 2), dtype='object')
        copies = []
        i = 0
        for idx in res:
            for user in self.recommendations:
                ids = user.get_ids()
                mark = user.get_marks()[5]
                if idx == ids[0] and ids[1] not in own_rec and ids[1] not in copies and mark > lst[i, 1] and mark > 2:
                    lst[i, 0], lst[i, 1] = ids[1], mark
                    copies.append(ids[1])
            i += 1
        return lst[:, 0]

    @staticmethod
    def objects_to_replace(restaurants):
        lst = []
        for restaurant in restaurants:
            if isinstance(restaurant, Restaurant):
                lst.append(restaurant)
        lst = np.array(lst, dtype='object')
        return lst

    @staticmethod
    def objects_to_matrix(restaurants):
        lst = []
        names = []
        for restaurant in restaurants:
            if isinstance(restaurant, Restaurant):
                lst.append(restaurant.get_numerical_parameters())
                names.append(restaurant)
        lst = np.array(lst, dtype='float')
        return lst, names

    @staticmethod
    def norm_2_st_2(m):
        out = np.zeros(m.shape[1])
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                out[j] += (m[i, j]) ** 2
        for i in range(len(out)):
            out[i] = math.sqrt(out[i])
        return out

    @staticmethod
    def norm_2_st_5(m, w):
        out = 0
        for i in range(m.shape[0]):
            out += (m[i] - w[i]) ** 2
        return math.sqrt(out)

    def topsis(self, matrix, weights, res, ocassion):
        if ocassion:
            crit = [1, 0, 1, 1, 1, 1]
        else:
            crit = [1, 0, 1, 1, 0, 1]
        M = deepcopy(matrix)  # Step 1
        l_p = self.norm_2_st_2(M)  # Step 2
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                M[i, j] = M[i, j] / l_p[j]
        W = deepcopy(weights)  # Step 3
        W = W / sum(weights)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                M[i, j] *= W[j]
        ideal = np.zeros(M.shape[1])  # Step 4
        nadir = np.zeros(M.shape[1])
        for i in range(M.shape[1]):
            if crit[i]:
                ideal[i] = max(M[:, i])
                nadir[i] = min(M[:, i])
            else:
                ideal[i] = min(M[:, i])
                nadir[i] = max(M[:, i])
        best = np.zeros(M.shape[0])  # Step 5
        worst = np.zeros(M.shape[0])
        for i in range(M.shape[0]):
            best[i] = self.norm_2_st_5(M[i], ideal)
            worst[i] = self.norm_2_st_5(M[i], nadir)
        wsp_c = np.zeros(M.shape[0])  # Step 6
        for i in range(M.shape[0]):
            if (worst[i] + best[i]) == 0:
                wsp_c[i] = worst[i] / 0.0000001
            else:
                wsp_c[i] = worst[i] / (worst[i] + best[i])
        rank = np.array(sorted(list(zip(res, wsp_c)), key=lambda x: x[1], reverse=True), dtype='object')  # Step 7
        return rank[:, 0]

    @staticmethod
    def norm_2_st_2(m):
        out = np.zeros(m.shape[1])
        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                out[j] += (m[i, j]) ** 2
        for i in range(len(out)):
            out[i] = math.sqrt(out[i])
        return out

    @staticmethod
    def norm_2_st_5(m, w):
        out = 0
        for i in range(m.shape[0]):
            out += (m[i] - w[i]) ** 2
        return math.sqrt(out)

    def RSM(self, matrix, weights, res, target_points, status_quo):
        M = deepcopy(matrix)
        l_p = self.norm_2_st_2(M)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                M[i, j] = M[i, j] / l_p[j]
        W = deepcopy(weights)
        W = W / sum(weights)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                M[i, j] *= W[j]
        l_p_t = self.norm_2_st_2(target_points)
        l_p_q = self.norm_2_st_2(status_quo)
        for i in range(target_points.shape[0]):
            for j in range(target_points.shape[1]):
                target_points[i, j] = target_points[i, j] / l_p_t[j]
                target_points[i, j] *= W[j]
                status_quo[i, j] = status_quo[i, j] / l_p_q[j]
                status_quo[i, j] *= W[j]
        final_target = np.zeros(M.shape[1])
        final_status_quo = np.zeros(M.shape[1])
        for i in range(M.shape[1]):
            final_target[i] = sum(target_points[:, i]) / target_points.shape[0]
            final_status_quo[i] = sum(status_quo[:, i]) / status_quo.shape[0]
        best = np.zeros(M.shape[0])
        worst = np.zeros(M.shape[0])
        for i in range(M.shape[0]):
            best[i] = self.norm_2_st_5(M[i], final_target)
            worst[i] = self.norm_2_st_5(M[i], final_status_quo)
        wsp_c = np.zeros(M.shape[0])
        for i in range(M.shape[0]):
            wsp_c[i] = worst[i] / (worst[i] + best[i])
        rank = np.array(sorted(list(zip(res, wsp_c)), key=lambda x: x[1], reverse=True), dtype='object')
        return rank[:, 0]


restaurants = []
recommendations = []
recommendation_system = CollaborativeFiltering(restaurants, recommendations)
recommendation_system.upload_restaurants_marks()
recommendation_system.upload_own_recommendations()
