import streamlit as st
import pandas as pd
import numpy as np
import itertools

st.title("Preping meals just became easy!")
df = pd.DataFrame({
    'recipe_name': ['palak paneer', 'paneer butter masala', 'cabbage carrot peas sabzi', 'burritto bowl'],
    'ingredients': [['spinach', 'paneer', 'tomato', 'onion'], ['paneer', 'onion', 'tomato'], ['cabbage', 'corrot', 'peas'], ['beans', 'avocado', 'sour cream', 'lettuce']],
    'cuisine': ['indian', 'indian', 'indian', 'mexican']
})

unique_ingredients = np.unique(list(itertools.chain.from_iterable(df['ingredients'].values)))
unique_cuisine = df['cuisine'].unique().tolist()
number_of_recipes = st.number_input("How many dishes do you want to make this week?", 0, 3, value=2)
cuisine_pref = st.multiselect("Any  cuisine preference?", unique_cuisine)
ingredient_pref = st.multiselect('Any ingredient preference?', unique_ingredients)

if number_of_recipes == 0:
    number_of_recipes = 2

if len(cuisine_pref)>0:
    df_cuisine = [df['cuisine'].isin(cuisine_pref)]
else:
    df_cuisine = pd.Series([True]*df.shape[0])

if len(ingredient_pref):
    df_ingre = df.apply(lambda x: any(item in ingredient_pref for item in x['ingredients']), axis=1)
else:
    df_ingre = pd.Series([True]*df.shape[0])

df_cuisine_t = df_cuisine[df_cuisine==True]
df_recommend = df.iloc[df_ingre[df_cuisine_t][df_ingre[df_cuisine_t==True]].index.tolist()].reset_index(drop=True)

if df_recommend.shape[0]>0:
    st.header('Find recommendations below:')
    st.dataframe(df_recommend.iloc[:number_of_recipes])
else:
    st.write('No recipes that satisfy your filters!')

st.header('Add your new recipes here:')
recipe_name = st.text_input("What's the recipe name?")
ingredients = st.text_input("What are the major ingredients (comma spaced)? ")
ingredients = ingredients.split(',')
cuisine = st.text_input("What is the cuisine?")

df.append({'recipe_name': recipe_name, 'ingredients': ingredients, 'cuisine': cuisine}, ignore_index=True)
st.write(df)

