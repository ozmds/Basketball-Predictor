from datetime import datetime
import locators
from common import create_driver, get_beautiful_soup, write_csv_with_headers


def convert_to_datetime(game_date, game_time):
    if game_time[-1] == 'p':
        game_time = game_time[:-1] + 'PM'
    else:
        game_time = game_time[:-1] + 'AM'
    return datetime.strptime(game_date + ' ' + game_time, '%a, %b %d, %Y %I:%M%p')


def format_game(game):
    game_date = game.select('[data-stat="date_game"]')[0].string
    game_time = game.select('[data-stat="game_start_time"]')[0].string
    visitor_team = game.select('[data-stat="visitor_team_name"]')[0].string
    visitor_score = game.select('[data-stat="visitor_pts"]')[0].string
    home_team = game.select('[data-stat="home_team_name"]')[0].string
    home_score = game.select('[data-stat="home_pts"]')[0].string
    game_url = game.select('[data-stat="box_score_text"] > a')[0]['href']
    overtime = game.select('[data-stat="overtimes"]')[0].string
    return {
        'Game Date': convert_to_datetime(game_date, game_time).strftime('%d-%m-%Y %H:%M'),
        'Visitor': visitor_team,
        'Visitor Score': visitor_score,
        'Home': home_team,
        'Home Score': home_score,
        'Game URL': locators.BASE_URL + game_url,
        'OT': overtime
    }


def get_all_games(driver, year):
    url = locators.BASE_URL + locators.LEAGUE_GAMES_BASE_URL.format(year)
    soup = get_beautiful_soup(driver, url)
    month_urls = list(map(lambda x: locators.BASE_URL + x['href'], soup.select(locators.MONTH_SELECTOR)))
    game_list = []
    for i, month_url in enumerate(month_urls):
        soup = get_beautiful_soup(driver, month_url)
        game_content = soup.select(locators.GAME_SELECTOR)
        for j, game in enumerate(game_content):
            print(i, j)
            if len(game.select('[data-stat="box_score_text"] > a')) > 0:
                game_list.append(format_game(game))
            else:
                break
    return game_list


if __name__ == '__main__':
    driver = create_driver()
    game_list = get_all_games(driver, '2020')
    headers = ['Game Date', 'Visitor', 'Visitor Score', 'Home', 'Home Score', 'Game URL', 'OT']
    write_csv_with_headers('./output.csv', game_list, headers)
