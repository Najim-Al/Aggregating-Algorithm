# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 13:56:01 2021

@author: Owner
"""
import numpy as np
import  pandas as pd
from LossFunction import *

def squared_loss(outcome, prediction):
    loss = (prediction - outcome)**2
    return loss

def absoloute_loss(outcome, prediction):
    loss = abs(prediction - outcome)
    return loss

# AA's have equal inital experts weights 

def AA(outcomes, prediction, loss, learning_rate):
    T = len(outcomes)
    N_experts = np.size(prediction,1)
    weights = np.ones(N_experts)
    learner_prediction = np.zeros(T)
    loss_log = np.zeros((T, N_experts))
    learner_loss = np.zeros(T)
    for t in range(T):
        print(t)
        norm_weights = weights / sum(weights)
        learner_prediction[t] = sum( norm_weights * prediction[t] )
        learner_loss[t] = loss(outcomes[t],learner_prediction[t])
        for i in range(N_experts):
            loss_log[t,i] = loss(outcomes[t],prediction[t,i])
            weights[i] = weights[i] * np.exp(-learning_rate*loss_log[t,i]) #+ 0.5    
    return learner_loss, loss_log, learner_prediction

def AA_Class(outcomes, prediction, loss: LossFunc, learning_rate):
    T = len(outcomes)
    N_experts = np.size(prediction,1)
    weights = np.ones(N_experts)
    learner_prediction = np.zeros(T)
    loss_log = np.zeros((T, N_experts))
    weight_log = np.zeros((T, N_experts))
    learner_loss = np.zeros(T)
    for t in range(T):
        if np.isnan(sum(weights)):
            break
        print(t)
#        if t % 1000 == 0:
#            weights = np.ones(N_experts)
        norm_weights = weights / sum(weights)
        learner_prediction[t] = sum( norm_weights * prediction[t] )
        learner_loss[t] = loss.calc_loss(outcomes[t],learner_prediction[t]) 
        for i in range(N_experts):
            loss_log[t,i] = loss.calc_loss(outcomes[t],prediction[t,i]) 
            weights[i] = weights[i] * np.exp(-learning_rate*loss_log[t,i]) #+ 0.5    
        #    if np.isnan(weights[i]):
         #       weights[i] =1
            weight_log[t] = weights
            
    return learner_loss, loss_log, learner_prediction, loss ,weight_log

def weak_AA_class(outcomes, prediction, loss: LossFunc, learning_rate):
    T = len(outcomes)
    N_experts = np.size(prediction,1)
    norm_weights = np.ones(N_experts)
    learner_prediction = np.zeros(T)
    loss_log = np.zeros((T, N_experts))
    cumsum_loss = np.zeros(N_experts)
    learner_loss = np.zeros(T)
    for t in range(1, T):
        print(t)
        #if t % 1000 == 0:
         #   weights = np.ones(N_experts)
        learner_prediction[t] = sum( norm_weights * prediction[t] )
        learner_loss[t] = loss.calc_loss(outcomes[t],learner_prediction[t])
        denominator = 0
        for j in range(N_experts):
                denominator +=  np.exp(-learning_rate*cumsum_loss[j])
        for i in range(N_experts):
            norm_weights[i] = np.exp(-learning_rate*cumsum_loss[i]) / denominator
            loss_log[t,i] = loss.calc_loss(outcomes[t],prediction[t,i])
            cumsum_loss += loss_log[t,:]
    return learner_loss, loss_log, learner_prediction

def weak_AA(outcomes, prediction, loss, learning_rate):
    T = len(outcomes)
    N_experts = np.size(prediction,1)
    norm_weights = np.ones(N_experts)
    learner_prediction = np.zeros(T)
    loss_log = np.zeros((T, N_experts))
    cumsum_loss = np.zeros(N_experts)
    learner_loss = np.zeros(T)
    for t in range(1, T):
        print(t)
        learner_prediction[t] = sum( norm_weights * prediction[t] )
        learner_loss[t] = loss(outcomes[t],learner_prediction[t])
        for i in range(N_experts):
            denominator = 0
            for j in range(N_experts):
                denominator +=  np.exp(-learning_rate*cumsum_loss[j])
            norm_weights[i] = np.exp(-learning_rate*cumsum_loss[i]) / denominator
            loss_log[t,i] = loss(outcomes[t],prediction[t,i])
            cumsum_loss += loss_log[t,:]
    return learner_loss, loss_log, learner_prediction

def squash(ratio, S, offset):
    return offset + (1 / (1+ np.exp(-S *(ratio))))

#change
if __name__ ==  '__main__':
    data = pd.read_csv(r"C:\Users\Owner\Downloads\tennis1 (1).txt", sep='\s+')
    outs = data.iloc[:,1]
    p1 = data.iloc[:,3]
    p2 = data.iloc[:,5]
    p3 = data.iloc[:,7]
    p4 = data.iloc[:,9]
    pred = pd.concat([p1,p2, p3, p4], axis =1)
    
    lossfun = squaredLoss(outs.values, pred.values)
    AA_loss, experts_loss, pred_learner = AA_Class(outs.values, pred.values, lossfun, 2)
    WAA_loss, Wexperts_loss, Wpred_learner = weak_AA_class(outs.values, pred.values, lossfun, 2)
    
    