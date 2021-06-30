#Maayan Popovsky

import requests_html

def creat_the_correct_url(movie_titles):
    return "https://www.imdb.com/find?s=tt&q=" + movie_titles + "&ref_=nv_sr_sm"

def find_the_movie_list_line(data):
    array = data.split('\n')
    flag_table_class = False
    for line in array:
        if (line == '<table class="findList">'):
            flag_table_class = True
            continue
        if flag_table_class:
            return line

def is_in_development(movie_details_res):
    director_stars_data = movie_details_res.html.find('[data-testid="hero-subnav-bar-imdb-pro-link"]')
    if (director_stars_data != []):
        if ("In development" in director_stars_data[0].text):
            return False
        else:
            return True
    else: #In a situation where the data is not available
        return True

def the_relevant_data(tr):
    split_tr = tr.split('> <')
    split_movie_titles = split_tr[5].split('>')
    movie_url = split_movie_titles[0]
    movie_name = split_movie_titles[1]

    movie_url_arr = movie_url.split('"')
    movie_url = movie_url_arr[1]

    movie_name_arr = movie_name.split('<')
    movie_name = movie_name_arr[0]

    return (movie_url, movie_name)

def if_contain_alpha(str):
    for s in str:
        if s.isalpha():
            return True
    return False

def get_genre(data):
    data_array = data.split("genre")
    if (len(data_array) < 2):
        return ""
    genre_str = data_array[1]
    gener_arr = genre_str[0:genre_str.find(']')].split('"')

    if ("[" not in gener_arr[1]):  # If there is only one genre
        return gener_arr[2]
    genre_str = ""
    for str in gener_arr:
        if (if_contain_alpha(str)):
            genre_str += str + ", "
        else:
            if ("]" in str):
                return (genre_str[0:len(genre_str) - 2])

    return (genre_str[0:len(genre_str) - 2])

def get_rating(data):
    data_array = data.split("contentRating")
    if (len(data_array) < 2):
        return ""
    rating_value_arr = data_array[1].split('"')
    return rating_value_arr[2]

def get_duration(data):
    data_array = data.split("duration")
    if (len(data_array) < 2):
        return ""
    duration_value_arr = data_array[1].split('"')
    duration_value = duration_value_arr[2]
    duration_value = duration_value.replace("PT", "")
    duration_value = duration_value.replace("H", "h ")
    duration_value = duration_value.replace("M", "min ")
    return duration_value

def get_director(data):
    for i in data:
        i_text = i.text
        if (i_text.startswith("Director")):
            director_list = i_text.replace("Director", "")
            director_list = director_list.replace("\n", ", ")
            return director_list[2:len(director_list)]
    return ""

def get_star(data):
    for i in data:
        i_text = i.text
        if (i_text.startswith("Star")):
            star_list = i_text.replace("Star", "")
            star_list = star_list.replace("\n", ", ")
            return star_list[2:len(star_list)]
    return ""

def checks_if_has_value(value):
    if (value != ""):
        return "|" + value
    else:
        return ""

def main():
    movie_titles = input('Please insert your movie titles: ')
    print("Thanks!")
    correct_url = creat_the_correct_url(movie_titles)
    session = requests_html.HTMLSession()
    res = session.get(correct_url)
    data = res.html.html
    movie_list_line = find_the_movie_list_line(data)
    split_movie_list_line = movie_list_line.split('<tr')
    result_file = open(movie_titles+" result file.txt", "w", encoding="utf-8")
    print("In process...")

    for tr in split_movie_list_line:
        if (len(tr) > 1):
            (movie_url, movie_name) = the_relevant_data(tr)

            if ((" " + movie_titles + " ").lower() in (
                    " " + movie_name.lower() + " ")):  # Checking if the movie name is correct
                movie_details_res = session.get("https://www.imdb.com" + movie_url)

                if (is_in_development(movie_details_res)):
                    director_stars_data = movie_details_res.html.find("li")
                    movie_details_html = movie_details_res.html.html
                    movie_details_split = movie_details_html.split("<script")

                    for i in movie_details_split:
                        if (' type="application/ld+json"' in i):
                            all_Details = movie_name

                            genre = get_genre(i)
                            all_Details += checks_if_has_value(genre)

                            rating = get_rating(i)
                            all_Details += checks_if_has_value(rating)

                            duration = get_duration(i)
                            all_Details += checks_if_has_value(duration)

                            director = get_director(director_stars_data)
                            all_Details += checks_if_has_value(director)

                            star = get_star(director_stars_data)
                            all_Details += checks_if_has_value(star)

                            all_Details = all_Details.strip('\n')

                            result_file.write(all_Details + "\n")

    result_file.close()
    print('The file with the information about the movies with the titles "'+movie_titles+'" is ready')
    print('The file name is: '+movie_titles+' result file.txt')


if __name__ == '__main__':
    main()
