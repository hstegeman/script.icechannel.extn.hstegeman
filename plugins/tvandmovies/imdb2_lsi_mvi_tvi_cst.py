'''
    IMDb2
    28-6-2015
'''

from entertainment.plugnplay.interfaces import ListIndexer
from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc,os

class IMDb(MovieIndexer, TVShowIndexer, CustomSettings, ListIndexer):
    implements = [MovieIndexer, TVShowIndexer, CustomSettings, ListIndexer]

    name = "IMDb2"
    display_name = "IMDb2"

    img='https://istream-xbmc-repo.googlecode.com/svn/images/imdb.png'
    
    default_indexer_enabled = 'true'

    def __init__(self):

        minimum_votes_list = '100000|50000|25000|15000|10000|7500|5000|3000|1500|1000|500|200|100|50|25|10|5|1|0'
        maximum_moviemeter_list = '500|1000|2000|5000|7500|10000|25000|50000|100000|200000|0'
        SortByOptions_list = 'alpha|user_rating|boxoffice_gross_us|moviemeter|num_votes|release_date_us'
        SortByOptions_tv_list = 'alpha|user_rating|moviemeter|num_votes|release_date_us'
        SortByOptions_charts_list = 'ir|nv|rd'
        SortByOptions_People_list = 'alpha|starmeter|height|birth_date|death_date'
        SortByOptions_Watchlist = 'list_order|alpha|user_rating|moviemeter|num_votes|release_date_us|date_added'
        page_item_count_list = '30|50|100|200|250'
        pages_count_list = '-|1|5|10|20|25|50|100'
        days_count_list = '-|1|2|3'
        boxoffice_gross_us_list = '1|10000|100000|1000000|10000000'
        production_status_list = 'released|active|released,active'
        now_playing_weeks_us_list = '5|10|20|25|50|100|200|250|500|1000|5000|10000'

        xml = '<settings>\n'
        xml += '<category label="IMDb SETTINGS">\n'
        xml += '<setting id="en_us" type="bool" label="Show English Language Only" default="true" />\n'
        xml += '<setting id="get_url()" label="Base Url" type="labelenum" default="http://imdb.com/" values="http://imdb.com/|http://akas.imdb.com/" />\n'
        xml += '<setting id="get_m_url()" label="Base Url Mobile" type="labelenum" default="http://m.imdb.com/" values="http://m.imdb.com/" />\n'
        xml += '<setting id="imdb_user_number" label="User Number" type="text" default="" />\n'
        xml += '<setting id="future" type="bool" label="Show Future Episodes" default="false" />\n'
        xml += '<setting id="page_item_count" label="Page item count" type="labelenum" default="100" values=' + page_item_count_list + ' />\n'
        xml += '<setting id="maximum_pages_count" label="Maximum pages count" type="labelenum" default="10" values=' + pages_count_list + ' />\n'
        xml += '<setting id="page_people_item_count" label="Page item count People" type="labelenum" default="100" values="50|100" />\n'
        xml += '<setting id="maximum_people_pages_count" label="Maximum People pages count" type="labelenum" default="10" values=' + pages_count_list + ' />\n'
        xml += '<setting id="subscripions_delay_days" label="Set Subscription delay in days" type="labelenum" default="1" values=' + days_count_list + ' />\n'
        xml += '<setting id="exclude_seen_movies_tvshows" type="bool" label="Exclude Seen Movies / TV Shows" default="false" />\n'
        xml += '<setting id="imdb_userlist_number" label="IMDB UserList Number Exclude Seen Movies/TV Shows" type="text" default="" />\n'
        xml += '</category>\n'
        xml += '<category label="MOVIE FILTERS">\n'
        xml += '<setting id="movie_votes_regular" label="Minimum votes, most popular, most voted" type="labelenum" default="3000" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="movie_votes_less" label="Minimum votes, decade, genres" type="labelenum" default="1000" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="movie_votes_small" label="Minimum votes, year, keyword" type="labelenum" default="500" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="movie_votes_rated" label="Minimum votes, highly rated" type="labelenum" default="25000" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="movie_votes_rated_subs" label="Minimum votes, highly rated subs" type="labelenum" default="10000" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="movie_meter_regular" label="Maximum moviemeter, regular" type="labelenum" default="50000" values=' + maximum_moviemeter_list + ' />\n'
        xml += '<setting id="movie_meter_less" label="Maximum moviemeter, less" type="labelenum" default="200000" values=' + maximum_moviemeter_list + ' />\n'
        xml += '<setting id="movie_minimum_boxoffice_gross_us" label="Minimum boxoffice" type="labelenum" default="10000" values=' + boxoffice_gross_us_list + ' />\n'
        xml += '<setting id="now_playing_weeks_us" label="Now Playing Weeks US" type="labelenum" default="100" values=' + now_playing_weeks_us_list + ' />\n'
        xml += '<setting id="movie_GetSortByOptions" label="Main Sort By Option Movies" type="labelenum" default="boxoffice_gross_us" values=' + SortByOptions_list + ' />\n'
        xml += '<setting id="movie_GetSortOrderOptions" label="Main Sort Order Option Movies" type="labelenum" default="desc" values="asc|desc" />\n'
        xml += '<setting id="movie_GetSortByOptions_now_playing_us" label="Main Sort By Option Movies Now Playing US" type="labelenum" default="release_date_us" values=' + SortByOptions_list + ' />\n'
        xml += '<setting id="movie_GetSortOrderOptions_now_playing_us" label="Main Sort Order Option Movies Now Playing US" type="labelenum" default="desc" values="asc|desc" />\n'
        xml += '<setting id="movie_GetSortByOptions_tv" label="Main Sort By Option TV Movie" type="labelenum" default="num_votes" values=' + SortByOptions_tv_list + ' />\n'
        xml += '<setting id="movie_GetSortOrderOptions_tv" label="Main Sort Order Option TV Movie" type="labelenum" default="desc" values="asc|desc" />\n'
        xml += '</category>\n'
        xml += '<category label="TVSHOW FILTERS">\n'
        xml += '<setting id="tvshow_votes_regular" label="Minimum votes, most popular, most voted" type="labelenum" default="3000" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="tvshow_votes_less" label="Minimum votes, decade, genres" type="labelenum" default="1000" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="tvshow_votes_small" label="Minimum votes, year, keyword" type="labelenum" default="500" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="tvshow_votes_rated" label="Minimum votes, highly rated" type="labelenum" default="5000" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="tvshow_votes_rated_subs" label="Minimum votes, highly rated subs" type="labelenum" default="5000" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="tvshow_meter_regular" label="Maximum moviemeter, regular" type="labelenum" default="50000" values=' + maximum_moviemeter_list + ' />\n'
        xml += '<setting id="tvshow_meter_less" label="Maximum moviemeter, less" type="labelenum" default="200000" values=' + maximum_moviemeter_list + ' />\n'
        xml += '<setting id="tvshow_production_status" label="Production status TV Shows" type="labelenum" default="released,active" values=' + production_status_list + ' />\n'
        xml += '<setting id="tvshow_GetSortByOptions" label="Main Sort By Option TV Shows" type="labelenum" default="num_votes" values=' + SortByOptions_tv_list + ' />\n'
        xml += '<setting id="tvshow_GetSortOrderOptions" label="Main Sort Order Option TV Shows" type="labelenum" default="desc" values="asc|desc" />\n'
        xml += '</category>\n'
        xml += '<category label="AWARDS FILTERS">\n'
        xml += '<setting id="movie_GetSortByOptions_awards" label="Main Sort By Option Awards Movies" type="labelenum" default="boxoffice_gross_us" values=' + SortByOptions_list + ' />\n'
        xml += '<setting id="movie_GetSortOrderOptions_awards" label="Main Sort Order Option Awards Movies" type="labelenum" default="desc" values="asc|desc" />\n'
        xml += '<setting id="movie_GetSortByOptions_awards_tv" label="Main Sort By Option Awards TV Movie" type="labelenum" default="num_votes" values=' + SortByOptions_tv_list + ' />\n'
        xml += '<setting id="movie_GetSortOrderOptions_awards_tv" label="Main Sort Order Option Awards TV Movie" type="labelenum" default="desc" values="asc|desc" />\n'
        xml += '<setting id="tvshow_GetSortByOptions_awards" label="Main Sort By Option Awards TV Shows" type="labelenum" default="num_votes" values=' + SortByOptions_tv_list + ' />\n'
        xml += '<setting id="tvshow_GetSortOrderOptions_awards" label="Main Sort Order Option Awards TV Shows" type="labelenum" default="desc" values="asc|desc" />\n'
        xml += '</category>\n'
        xml += '<category label="IMDB Ratings FILTERS">\n'
        xml += '<setting id="movie_GetSortByOptions_imdb_ratings_charts" label="Main Sort By Option IMDB Ratings Charts" type="labelenum" default="ir" values=' + SortByOptions_charts_list + ' />\n'
        xml += '<setting id="movie_GetSortOrderOptions_imdb_ratings_charts" label="Main Sort Order IMDB Ratings Charts" type="labelenum" default="desc" values="asc|desc" />\n'
        xml += '<setting id="movie_GetSortByOptions_imdb_ratings" label="Main Sort By Option IMDB Ratings" type="labelenum" default="user_rating" values=' + SortByOptions_list + ' />\n'
        xml += '<setting id="movie_GetSortOrderOptions_imdb_ratings" label="Main Sort Order IMDB Ratings" type="labelenum" default="desc" values="asc|desc" />\n'
        xml += '<setting id="movie_GetSortByOptions_imdb_ratings_bottom" label="Main Sort By Option IMDB Ratings Bottom" type="labelenum" default="user_rating" values=' + SortByOptions_list + ' />\n'
        xml += '<setting id="movie_GetSortOrderOptions_imdb_ratings_bottom" label="Main Sort Order IMDB Ratings Bottom" type="labelenum" default="asc" values="asc|desc" />\n'
        xml += '</category>\n'
        xml += '<category label="LANGUAGE FILTERS">\n'
        xml += '<setting id="movie_votes_language" label="Minimum votes Movies, language" type="labelenum" default="100" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="movie_votes_rated_language" label="Minimum votes  Movies, highly rated language" type="labelenum" default="1000" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="movie_GetSortByOptions_language" label="Main Sort By Option Movies language" type="labelenum" default="num_votes" values=' + SortByOptions_list + ' />\n'
        xml += '<setting id="movie_GetSortOrderOptions_language" label="Main Sort Order Option Movies language" type="labelenum" default="desc" values="asc|desc" />\n'
        xml += '<setting id="tvshow_votes_language" label="Minimum votes TV Shows, language" type="labelenum" default="50" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="tvshow_votes_rated_language" label="Minimum votes TV Shows, highly rated language" type="labelenum" default="200" values=' + minimum_votes_list + ' />\n'
        xml += '<setting id="tvshow_GetSortByOptions_language" label="Main Sort By Option TV Shows language" type="labelenum" default="num_votes" values=' + SortByOptions_tv_list + ' />\n'
        xml += '<setting id="tvshow_GetSortOrderOptions_language" label="Main Sort Order Option TV Shows language" type="labelenum" default="desc" values="asc|desc" />\n'
        xml += '</category>\n'
        xml += '<category label="WATCHLIST FILTERS">\n'
        xml += '<setting id="watchlist_GetSortByOptions" label="Main Sort By Option Watchlists" type="labelenum" default="moviemeter" values=' + SortByOptions_Watchlist + ' />\n'
        xml += '<setting id="watchlist_GetSortOrderOptions" label="Main Sort Order Option Watchlists" type="labelenum" default="asc" values="asc|desc" />\n'
        xml += '</category>\n'
        xml += '<category label="USERLIST FILTERS">\n'
        xml += '<setting id="userlist_GetSortByOptions" label="Main Sort By Option Userlists" type="labelenum" default="moviemeter" values=' + SortByOptions_list + ' />\n'
        xml += '<setting id="userlist_GetSortOrderOptions" label="Main Sort Order Option Userlists" type="labelenum" default="asc" values="asc|desc" />\n'
        xml += '<setting id="userlist_People_GetSortByOptions" label="Main Sort By Option Userlists People" type="labelenum" default="starmeter" values=' + SortByOptions_People_list + ' />\n'
        xml += '<setting id="userlist_People_GetSortOrderOptions" label="Main Sort Order Option Userlists People" type="labelenum" default="asc" values="asc|desc" />\n'
        xml += '</category>\n'
        xml += '<category label="INTERFACE">\n'
        xml += '<setting id="ShowSortByOptions" type="bool" label="Show Main Sort By Option" default="false" />\n'
        xml += '<setting id="watch_list_main" type="bool" label="Show Main Watchlist" default="true" />\n'
        xml += '<setting id="moviemeter" type="bool" label="Most Popular" default="true" />\n'
        xml += '<setting id="boxoffice_gross_us" type="bool" label="Box Office" default="true" />\n'
        xml += '<setting id="genres" type="bool" label="Genres" default="true" />\n'
        xml += '<setting id="genres_submenu" type="bool" label="Genres Submenu" default="true" />\n'
        xml += '<setting id="year" type="bool" label="Year" default="true" />\n'
        xml += '<setting id="decade" type="bool" label="Decade" default="true" />\n'
        xml += '<setting id="now-playing-us" type="bool" label="Now Playing" default="true" />\n'
        xml += '<setting id="user_rating" type="bool" label="Highly Rated" default="true" />\n'
        xml += '<setting id="num_votes" type="bool" label="Most Voted" default="true" />\n'
        xml += '<setting id="additional" type="bool" label="Additional" default="true" />\n'
        xml += '<setting id="award" type="bool" label="Awards" default="true" />\n'
        xml += '<setting id="certificates" type="bool" label="Certificate" default="true" />\n'
        xml += '<setting id="company" type="bool" label="Company" default="true" />\n'
        xml += '<setting id="genres_all" type="bool" label="Genres All" default="true" />\n'
        xml += '<setting id="imdb_ratings" type="bool" label="IMDB Ratings" default="true" />\n'
        xml += '<setting id="imdb_ratings_imdb_top_250" type="bool" label="Highly Rated IMDB Top 250" default="true" />\n'
        xml += '<setting id="imdb_user_picks" type="bool" label="Imdb Userlists" default="true" />\n'
        xml += '<setting id="languages" type="bool" label="Language" default="true" />\n'
        xml += '<setting id="languages_Less-Common" type="bool" label="Less-Common Language" default="true" />\n'
        xml += '<setting id="theaters" type="bool" label="Theaters" default="true" />\n'
        xml += '<setting id="topboxoffice" type="bool" label="US Box Office" default="true" />\n'
        xml += '<setting id="theaters_soon" type="bool" label="Theaters: Coming Soon" default="true" />\n'
        xml += '<setting id="title_type" type="bool" label="Title Type" default="true" />\n'
        xml += '<setting id="people" type="bool" label="Peoples" default="true" />\n'
        xml += '<setting id="search_celeb" type="bool" label="Search Celebrity" default="true" />\n'
        xml += '</category>\n'
        xml += '</settings>\n'

        self.CreateSettings(self.name, self.display_name, xml)

    def get_url(self):
        return self.Settings().get_setting('get_url()')

    def get_m_url(self):
        return self.Settings().get_setting('get_m_url()')

    def get_json_date_total_count(self, content, page, page_item_count, int_weeks=1):
        import json
        import datetime
        i = 0
        data = json.loads(content)
        match = data['list']

        todays_date = datetime.date.today()
        next_date = todays_date + datetime.timedelta(weeks=int_weeks)
        next_date_time = datetime.datetime(next_date.year, next_date.month, next_date.day)

        start_index = (int(page)-1) * page_item_count
        match = match[start_index : start_index + page_item_count]

        for item in match:
            i=i+1
            item_title = ''
            try:
                item_title = item['title']
            except:
                item_header = item['header']

                item_header_date_time = self.get_formated_date(item_header)
                if item_header_date_time > next_date_time: break

        total_count = i
        return total_count

    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        import urllib

        if section == 'search_celeb':
            import xbmc
            search_entered = ''
            keyboard = xbmc.Keyboard(search_entered, '[COLOR blue]i[/COLOR]Stream')
            keyboard.doModal()
            if keyboard.isConfirmed():
                search_entered = keyboard.getText()
            if search_entered=='':return    
            url = urllib.unquote_plus(url+search_entered.replace(' ','+'))

        if section != 'search':
            url = urllib.unquote_plus(url)
        
        import re
        import json

        new_url = url

        if not new_url.startswith(self.get_url()):
            if not new_url.startswith(self.get_m_url()):
                new_url = re.sub("http\://.*?/", self.get_url(), url)

        if page == '':
            page = '1'

        default_page_item_count = self.Settings().get_setting('page_item_count')
        default_page_people_item_count = self.Settings().get_setting('page_people_item_count')
        maximum_pages_count = self.Settings().get_setting('maximum_pages_count')
        maximum_people_pages_count = self.Settings().get_setting('maximum_people_pages_count')
        total_count = 0

        if section == 'watchlist':
            page_item_count = 100
        elif section in ['gender','gender_episodes']:
            page_item_count = 50
        elif section in ['search_gender','search_gender_director','search_gender_actor','search_gender_writer','search_gender_producer','search_gender_soundtrack','search_gender_episodes','search_no_gender','search_no_gender_episodes']:
            page_item_count = int(default_page_people_item_count)
        else:
            page_item_count = int(default_page_item_count)

        start = str( ( (int(page) - 1) * page_item_count ) + 1 )
        count = str(page_item_count)

        print 'presume page ' + str(page)

        #reading out the original start=value from new_url.
        #if start value is not 1, then replace the start value.

        if section not in ['watchlist_people','json','json_date']:
            if not '?' in new_url:
                new_url = new_url + '?start=' + start + '&count=' + count
            elif '&start=' and '&end=' in new_url:
                new_url = new_url + '&view=simple' + '&count=' + count
            elif section in ['watchlist','search_gender','search_gender_director','search_gender_actor','search_gender_writer','search_gender_producer','search_gender_soundtrack','search_gender_episodes','search_no_gender','search_no_gender_episodes']:
                new_url = new_url + '&start=' + start + '&count=' + count
            elif section in ['gender']:
                new_url = new_url + '&page=' + str(page)
            else:
                new_url = new_url + '&start=' + start + '&view=simple' + '&count=' + count

        if section not in ['json','json_date']:
            print 'url 2 ' + new_url
            print 'sort_by ' + sort_by
            if sort_by == '' and 'sort' not in new_url:
                if indexer == common.indxr_Movies or indexer == common.indxr_Lists:
                    sort_by = self.Settings().get_setting('movie_GetSortByOptions')
                    movie_minimum_boxoffice_gross_us = self.Settings().get_setting('movie_minimum_boxoffice_gross_us')
                    if sort_by == 'boxoffice_gross_us':
                        new_url = new_url + '&boxoffice_gross_us=' + movie_minimum_boxoffice_gross_us + ','
                        url = url + '&boxoffice_gross_us=' + movie_minimum_boxoffice_gross_us + ','
                    elif sort_by == 'user_rating':
                        movie_votes_rated_subs = self.Settings().get_setting('movie_votes_rated_subs')
                        movie_votes_rated_language = self.Settings().get_setting('movie_votes_rated_language')

                        title_type_re = 'title_type=(.+?)&'
                        url_title_type = re.search(title_type_re, new_url)
                        votes_re = 'num_votes=(.+?),&'
                        url_votes = re.search(votes_re, new_url)

                        if url_votes:
                            movie_votes = url_votes.group(1)
                            if url_title_type:
                                movie_title_type = url_title_type.group(1)
                                if 'feature' in movie_title_type:
                                    new_url = new_url.replace('num_votes=' + movie_votes, 'num_votes=' + movie_votes_rated_subs)
                                    url = url.replace('num_votes=' + movie_votes, 'num_votes=' + movie_votes_rated_subs)
                                else:
                                    new_url = new_url.replace('num_votes=' + movie_votes, 'num_votes=' + movie_votes_rated_language)
                                    url = url.replace('num_votes=' + movie_votes, 'num_votes=' + movie_votes_rated_language)

                elif indexer == common.indxr_TV_Shows:
                    sort_by = self.Settings().get_setting('tvshow_GetSortByOptions')
                    if sort_by == 'user_rating':
                        tvshow_votes_rated_subs = self.Settings().get_setting('tvshow_votes_rated_subs')
                        votes_re = 'num_votes=(.+?),&'
                        url_votes = re.search(votes_re, new_url)
                        if url_votes:
                            tvshow_votes = url_votes.group(1)
                            new_url = new_url.replace('num_votes=' + tvshow_votes, 'num_votes=' + tvshow_votes_rated_subs)
                            url = url.replace('num_votes=' + tvshow_votes, 'num_votes=' + tvshow_votes_rated_subs)

            if sort_order == '' and 'sort' not in new_url:
                if indexer == common.indxr_Movies or indexer == common.indxr_Lists:
                    sort_order = self.Settings().get_setting('movie_GetSortOrderOptions')
                elif indexer == common.indxr_TV_Shows:
                    sort_order = self.Settings().get_setting('tvshow_GetSortOrderOptions')

            if 'sort' not in new_url:
                new_url = new_url + '&sort=' + ('title' if section == 'watchlist' and sort_by == 'alpha' else sort_by) + (':' if section == 'watchlist' else ',') + sort_order

        #making sort options available by setting sort_by and sort_order variables,
        #and delete the sort options from the original url.
        if section not in ['json','json_date']:
            if sort_by == '' and 'sort=' in new_url:
                sort_re = 'sort=(.+?),(.+?)&'
                url_sortings = re.search(sort_re, new_url)
                if url_sortings:
                    sort_by = url_sortings.group(1)
                    sort_order = url_sortings.group(2)
                    url = url.replace('sort=' + sort_by + ',' + sort_order, '')

        from entertainment.net import Net

        if section in ['watchlist','json','json_date','userlist','userlist_episodes']:
            cached = False
        else:
            cached = True
        net = Net(cached=cached)

        if self.Settings().get_setting('en_us')=='true':
            content = net.http_GET(new_url,{'Accept-Language':'en-US'}).content
        else:
            content = net.http_GET(new_url).content
        item_re = r'<a href="/title/(.+?)/">(.+?)</a>\n.+?<span class="year_type">(.+?)</span>'

        print 'http_GET ' + str(net.http_GET(new_url))
        #print 'content ' + content.encode('utf-8')

        print 'new_url ' + new_url
        if section == 'imdbcharts':
            item_re = r'<a href="/title/(.+?)/\?ref_=ch.+?"\ntitle=".+?" >(.+?)<.+?\n.+?class="secondaryInfo">(.+?)</span>'
            match=re.compile(item_re).findall(content)
            total_count = len(match)

            if page == '1' and start == '1':
                total_pages = str( total_count / page_item_count + ( 1 if total_count % page_item_count > 0 else 0 ) )

        if section in ['json','json_date']:
            if section == 'json':
                data = json.loads(content)
                match = data['list']
                total_count = len(match)
            else:
                total_count = self.get_json_date_total_count(content,page,page_item_count,int_weeks=1)

            if page == '1' and start == '1':
                total_pages = str( total_count / page_item_count + ( 1 if total_count % page_item_count > 0 else 0 ) )

        if total_pages == '':
            if section == 'watchlist':
                if not 'watchlist?' in new_url:
                    #not in use anymore, replaced by userlist.
                    re_page = '<span>\(([0-9,]+) of'
                else:
                    re_page = '(?s)<div class="desc">.+?([0-9,]+) titles'
            elif section in ['gender','gender_episodes']:
                re_page = '(?s)<div class="desc">.+?([0-9,]+) titles'
            else:
                re_page = '(?s)<div id="left">\n(.+?[0-9,]) of ([0-9,]+)'

            total_pages = re.search(re_page, content)
            if total_pages:
                if not section in ['watchlist','gender','gender_episodes']:
                    item_count = total_pages.group(1).split('-')[0]
                    item_count = int ( item_count.replace(',', '') )
                    total_count = total_pages.group(2)
                    #setting page number by making use of item count.
                    if item_count > 1:
                        page = str( item_count / page_item_count + ( 1 if item_count % page_item_count > 0 else 0 ) )
                else:
                    total_count = total_pages.group(1)
                    print 'presume total_count ' + str(total_count)

                total_count = int ( total_count.replace(',', '') )
                total_pages = str( total_count / page_item_count + ( 1 if total_count % page_item_count > 0 else 0 ) )

                if section in ['search_gender','search_gender_director','search_gender_actor','search_gender_writer','search_gender_producer','search_gender_soundtrack','search_gender_episodes','search_no_gender','search_no_gender_episodes']:
                    total_pages = str( total_count / page_item_count + ( 1 if total_count % page_item_count > 0 else 0 ) )
                    if maximum_people_pages_count != '-':
                        if int(total_pages) > int(maximum_people_pages_count):
                            total_pages = maximum_people_pages_count
                else:
                    total_pages = str( total_count / page_item_count + ( 1 if total_count % page_item_count > 0 else 0 ) )
                    if maximum_pages_count != '-':
                        if int(total_pages) > int(maximum_pages_count):
                            total_pages = maximum_pages_count
            else:
                if re.search('0 items found', content):
                    page = '0'
                    total_pages = '0'
                else:
                    page = '1'
                    total_pages = '1'

        '''
        print 'presume: addinfo:'
        #print 'indexer ' + indexer + '|section ' + section + '|type ' + type + '|page ' + page + '|total_pages ' + total_pages  + '|sort by ' + sort_by + '|sort order ' + sort_order
        print 'url ' + url
        print 'new_url content ' + new_url
        '''

        self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)

        mode = common.mode_File_Hosts
        if type == 'tv_shows':
            mode = common.mode_Content
            type = 'tv_seasons'

        if section == 'search_celeb':
            match=re.compile('<img src="(.+?)" /></a> </td> <td class="result_text"> <a href="(.+?)" >(.+?)<.+?<small>\((.+?),').findall(content)
            for img,url , name , gender in match:
                img=img.split(',')[0]
                if 'Actress' in gender or 'Actor' in gender:
                    self.AddSection(list, indexer, 'celeb_result', name+' (%s)'%gender, self.get_url()+url, indexer,img=img.replace('SX32','SX280'))

        if section == 'watchlist_people':
            match=re.compile('<a href="/(.+?)"><img src="(.+?)".+?alt="(.+?)">').findall(content)
            for url ,img, name in match:
                img=img.split(',')[0]
                self.AddSection(list, indexer, 'celeb_result', name, self.get_url()+url, indexer,img=img.replace('SX140','SX280'))

        if section == 'watchlist':
            if not 'watchlist?' in new_url:
                #not in use anymore, replaced by userlist.
                item_re = r'<a href="/title/(.+?)/">(.+?)</a>.+?<span class="year_type">(.+?)</span>'
            else:
                item_re= r'<a href="/title/(.+?)/.+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>'

        if section in ['gender']:
            item_re= r'<a href="/title/(.+?)/.+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>'

        if section in ['userlist_episodes']:
            item_re= r'<td class="title"><a href="/title/(.+?)/">(.+?)</a>\n.+?<span class="year_type">(.+?)</span><br>\n.+?<span class="episode">Episode: <a href="(.+?)">(.+?)</a>(.+?)</span>'

        if section in ['gender_episodes']:
            item_re= r'<h3 class="lister-item-header">\n.+?\n<a href="/title/(.+?)/.+?"\n>(.+?)</a>.+?<span class="lister-item-year text-muted unbold">(.+?)</span>\n.+?\n.+?<small class="text-primary unbold">Episode:</small>\n.+?<a href="(.+?)"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>'

        if section == 'topboxoffice':
            #not in use anymore, replaced by json.
            topboxoffice_re = '(?s)<h2>Top Box Office.+?<table(.+?)</table>'
            item_re = '<a href="/title/(.+?)\?ref_=cht_bo_.+?"\ntitle=".+?" >(.+?)<.+?\n.+?<span class="secondaryInfo">(.+?)</span>'
            topboxoffice_items = re.search(topboxoffice_re, content)
            if topboxoffice_items:
                content = topboxoffice_items.group(1)

        if section=='celeb_result':
            match=re.compile('<div class="filmo-row .+?" id=".+?">.+?span class="year_column">.+?nbsp;(.+?)</span>.+?<b><a href="/title/(.+?)/.+?>(.+?)</a>(.+?)<br/>',re.DOTALL).findall(content)
            for year , tt , title, id_type in match:

                if 'TV Series' in id_type:
                    type = 'tv_seasons'
                    mode = common.mode_Content
                    indexer = common.indxr_TV_Shows
                else:
                    type = common.indxr_Movies 
                    mode = common.mode_File_Hosts
                    indexer = common.indxr_Movies
                item_title = common.addon.unescape(title)
                item_url = self.get_url()+'title/'+tt+'/'
                year=year.strip()
                if '-' in year:
                    year=year.split('-')[0]
                self.AddContent(list, indexer, mode, item_title, '', type, url=item_url, name=item_title, year=year, imdb_id=tt)

        elif section in ['search_gender','search_gender_director','search_gender_actor','search_gender_writer','search_gender_producer','search_gender_soundtrack','search_gender_episodes','search_no_gender','search_no_gender_episodes']:
            item_re = r'<a href="/name/(.+?)/" title="(.+?)"><img src="(.+?)".+?\n.+?\n.+?\n.+?\n.+?<span class="description">(.+?),.+?">'
            match=re.compile(item_re).findall(content)

            import datetime

            # Get a date object
            todays_date = datetime.date.today()

            if indexer == common.indxr_Movies:
                url_type = 'title_type=movie,tvMovie&'
                movie_votes_language = self.Settings().get_setting('movie_votes_language')
                url_filter = '&num_votes=' + movie_votes_language + ',&release_date=,' + str(todays_date.year) + '&'
            elif indexer == common.indxr_TV_Shows:
                url_type = 'title_type=tvSeries,tvMiniSeries&'
                url_filter = '&release_date=,' + str(todays_date.year) + '&'
            elif indexer == common.indxr_Lists:
                url_type = 'title_type=movie,tvMovie,video,tvSpecial,short,movie,tvSeries,tvMiniSeries&'
                movie_votes_language = self.Settings().get_setting('movie_votes_language')
                url_filter = '&num_votes=' + movie_votes_language + ',&release_date=,' + str(todays_date.year) + '&'

            for url, name, img, gender in match:
                name = common.addon.unescape(name)
                img = str(img).split(',')[0]
                gender = str(gender).lower()

                if section in ['search_gender','search_gender_director','search_gender_writer','search_gender_producer','search_gender_soundtrack']:
                    if section == 'search_gender_director':
                        gender = 'director'
                    elif section == 'search_gender_writer':
                        gender = 'writer'
                    elif section == 'search_gender_producer':
                        gender = 'producer'
                    elif section == 'search_gender_soundtrack':
                        gender = 'soundtrack'

                    url_name = self.get_url()+'filmosearch?explore=title_type&role=' + url + url_filter + 'mode=advanced&job_type=' + gender + '&ref_=filmo_ref_job_typ&' + url_type + 'sort=release_date,desc'
                    self.AddSection(list, indexer, 'gender', name+' (%s)'%gender, url_name, indexer, img=img.replace('SX32','SX280'))

                elif section == 'search_gender_actor':
                    if 'actress' in gender or 'actor' in gender:
                        url_name = self.get_url()+'filmosearch?explore=title_type&role=' + url + url_filter + 'mode=advanced&job_type=' + gender + '&ref_=filmo_ref_job_typ&' + url_type + 'sort=release_date,desc'
                        self.AddSection(list, indexer, 'gender', name+' (%s)'%gender, url_name, indexer, img=img.replace('SX32','SX280'))
                elif section in ['search_no_gender']:
                    url_name = self.get_url()+'filmosearch?explore=title_type&role=' + url + url_filter + 'mode=advanced&ref_=filmo_ref_job_typ&' + url_type + 'sort=release_date,desc'
                    self.AddSection(list, indexer, 'gender', name+' (%s)'%gender, url_name, indexer, img=img.replace('SX32','SX280'))
                elif section in ['search_gender_episodes']:
                    if 'actress' in gender or 'actor' in gender:
                        url_type = 'title_type=tvEpisode&'
                        url_filter = '&num_votes=1,&release_date=,' + str(todays_date.year) + '&'
                        url_name = self.get_url()+'filmosearch?explore=title_type&role=' + url + url_filter + 'mode=advanced&job_type=' + gender + '&ref_=filmo_ref_job_typ&' + url_type + 'sort=release_date,desc'
                        self.AddSection(list, indexer, 'gender_episodes', name+' (%s)'%gender, url_name, indexer, img=img.replace('SX32','SX280'))
                elif section in ['search_no_gender_episodes']:
                    url_type = 'title_type=tvEpisode&'
                    url_filter = '&num_votes=1,&release_date=,' + str(todays_date.year) + '&'
                    url_name = self.get_url()+'filmosearch?explore=title_type&role=' + url + url_filter + 'mode=advanced&job_type=self&ref_=filmo_ref_job_typ&' + url_type + 'sort=release_date,desc'
                    self.AddSection(list, indexer, 'gender_episodes', name+' (%s)'%gender, url_name, indexer, img=img.replace('SX32','SX280'))

                print 'presume ' + url_name.encode('ascii', 'ignore')
                print 'presume ' + 'url ' + url.encode('ascii', 'ignore')
                print 'name ' + name.encode('ascii', 'ignore')
                print 'img ' + img.encode('ascii', 'ignore')
                print 'gender ' + gender.encode('ascii', 'ignore')
                #print 'presume ' + 'bio ' + bio.encode('ascii', 'ignore')
                #print 'presume ' + 'plot ' + plot.encode('ascii', 'ignore')

        elif section in ['json','json_date']:
            data = json.loads(content)
            match = data['list']
            start_index = (int(page)-1) * page_item_count
            match = match[start_index : start_index + page_item_count]

            if section in ['json_date']:
                if int(page_item_count) > int(total_count):
                    #cut match at total_count.
                    match = match[start_index : start_index + int(total_count)]

            for item in match:
                item_title = ''
                try:
                    item_title = common.addon.unescape(item['title']).encode('ascii', 'ignore')
                except:
                    item_header = item['header']

                if item_title != '':
                    item_v_id = item['url']
                    item_v_id=item_v_id.split('/')[2]
                    item_url = self.get_url()+'title/'+item_v_id+'/'
                    item_name = item_title
                    item_title = item_name

                    item_year = ''.join(x for x in item['extra'] if x.isdigit())
                    if item_year != '':
                        item_title = item_title + ' (' + item_year + ')'

                    if 'movie' in item['extra'].lower() or re.sub("[0-9]+", "", item['extra']) == "()":
                        type = common.indxr_Movies
                        mode = common.mode_File_Hosts
                        indexer = common.indxr_Movies
                    elif 'series' in item['extra'].lower() or ' ' in item['extra']:
                        type = 'tv_seasons'
                        mode = common.mode_Content
                        indexer = common.indxr_TV_Shows
                    else:
                        type = common.indxr_Movies
                        mode = common.mode_File_Hosts
                        indexer = common.indxr_Movies

                    '''
                    print 'presume addcontent json'
                    #print 'item indexer ' + str(indexer) + '|item mode ' + str(mode) + '|item_title ' + item_title + '|item type 2 ' + str(type) + '|item_name ' + item_name.encode('ascii', 'ignore') + '|item year ' + item_year + '|item imdb_id ' + str(item_v_id)
                    print 'item_url ' + str(item_url)
                    '''

                    if indexer == common.indxr_Movies:
                        self.AddContent(list, indexer, mode, item_title, '', type, url=item_url, name=item_name, year=item_year, imdb_id=item_v_id)
                    elif indexer == common.indxr_TV_Shows:
                        self.AddContent(list, indexer, mode, item_title, '', type, url=item_url, name=item_name, year=item_year, imdb_id=item_v_id)

        elif section in ['gender_episodes','userlist_episodes']:
            match=re.compile(item_re).findall(content)
            type = 'tv_episodes'
            mode = common.mode_File_Hosts
            indexer = common.indxr_TV_Shows

            for item_v_id, item_title, item_type, eps_v_id, eps_title, eps_type in match:
                item_title = item_title.encode('ascii', 'ignore')
                item_title = common.addon.unescape(item_title)
                item_type = item_type.encode('ascii', 'xmlcharrefreplace')
                item_type = item_type.replace('&#8211;', '-')
                item_year = re.search("\(([0-9]+)", item_type)

                if item_year:
                    item_year = item_year.group(1)
                else:
                    item_year = ''

                item_name = item_title
                eps_title = eps_title.encode('ascii', 'ignore')
                eps_title = common.addon.unescape(eps_title)
                eps_type = eps_type.encode('ascii', 'xmlcharrefreplace')
                eps_type = eps_type.replace('&#8211;', '-')
                eps_year = re.search("\(([0-9]+)", eps_type)

                if eps_year:
                    eps_year = eps_year.group(1)
                else:
                    eps_year = ''

                eps_url = self.get_url()+eps_v_id

                if total_pages == '':
                    total_pages = '1'

                import urllib
                eps_url = urllib.unquote_plus(eps_url)
                eps_title = urllib.unquote_plus(eps_title)
                item_name = urllib.unquote_plus(item_name)
                item_content = net.http_GET(eps_url).content
                item_eps_re = r'<span class="nobr">Season (.+?), Episode (.+?)\n.+?</span>'
                match_eps=re.compile(item_eps_re).findall(item_content)

                for season, eps_v_id in match_eps:
                    item_id = common.CreateIdFromString(item_name + '_' + item_year + '_season_' + season + '_episode_' + eps_v_id)
                    print 'item_id ' + item_id
                    print 'item_name ' + item_name
                    print 'presume addcontent 2'
                    print 'item indexer ' + str(indexer) + '|eps_title ' + eps_title + '|item_name ' + item_name + '|item year ' + item_year + '|season ' + str(season) + '|episode ' + str(eps_v_id)
                    print 'eps_url ' + str(eps_url)
                    self.AddContent(list, indexer, mode, eps_title, item_id, type, url=eps_url, name=item_name, year=item_year, season=season, episode=eps_v_id, imdb_id=item_v_id)

        else:

            if section in ['imdbcharts']:
                match=re.compile(item_re).findall(content)
                start_index = (int(page)-1) * page_item_count
                match = match[start_index : start_index + page_item_count]
            else:
                match=re.compile(item_re).findall(content)

            for item_v_id, item_title, item_type in match:
                item_title = item_title.encode('ascii', 'ignore')
                item_type = item_type.encode('ascii', 'xmlcharrefreplace')
                item_type = item_type.replace('&#8211;', '-')
                item_year = re.search("\(([0-9]+)", item_type)

                if item_year:
                    item_year = item_year.group(1)
                else:
                    item_year = ''
                if section in ['watchlist','gender']:
                    item_name = item_title
                else:
                    item_name = re.sub(" \([0-9]+.+?\)", "", item_title )
                item_title = item_name
                if item_year != '':
                    item_title = item_title + ' (' + item_year + ')'
                item_url = self.get_url()+'title/'+item_v_id+'/'
                if total_pages == '':
                    total_pages = '1'
                if section in ['watchlist','gender']:
                    if 'documentary' in item_type.lower():
                        type = common.indxr_Movies
                        mode = common.mode_File_Hosts
                        indexer = common.indxr_Movies
                    elif 'series' in item_type.lower() or '-' in item_type:
                        type = 'tv_seasons'
                        mode = common.mode_Content
                        indexer = common.indxr_TV_Shows
                    elif 'movie' in item_type.lower() or re.sub("[0-9]+", "", item_type) == "()":
                        type = common.indxr_Movies
                        mode = common.mode_File_Hosts
                        indexer = common.indxr_Movies
                    else:
                        type = common.indxr_Movies
                        mode = common.mode_File_Hosts
                        indexer = common.indxr_Movies
                else:
                    if 'documentary' in item_type.lower():
                        type = common.indxr_Movies
                        mode = common.mode_File_Hosts
                        indexer = common.indxr_Movies
                    elif 'series' in item_type.lower():
                        type = 'tv_seasons'
                        mode = common.mode_Content
                        indexer = common.indxr_TV_Shows
                    elif 'movie' in item_type.lower() or re.sub("[0-9]+", "", item_type) == "()":
                        type = common.indxr_Movies
                        mode = common.mode_File_Hosts
                        indexer = common.indxr_Movies
                    else:
                        type = common.indxr_Movies
                        mode = common.mode_File_Hosts
                        indexer = common.indxr_Movies

                print 'presume addcontent 2'
                print 'item indexer ' + str(indexer) + '|item mode ' + str(mode) + '|item_title ' + item_title + '|item type 2 ' + str(type) + '|item_name ' + item_name + '|item year ' + item_year + '|item imdb_id ' + str(item_v_id)
                print 'item type ' + item_type
                print 'item_url ' + str(item_url)
                self.AddContent(list, indexer, mode, item_title, '', type, url=item_url, name=item_name, year=item_year, imdb_id=item_v_id)

    def get_formated_date(self, date_str):
        
        import re
        import datetime
        
        item_air_date = common.unescape(date_str).replace('      ', '')
        item_fmtd_air_date = ""
        if 'Jan' in item_air_date: item_fmtd_air_date = '01-'
        elif 'Feb' in item_air_date: item_fmtd_air_date = '02-'
        elif 'Mar' in item_air_date: item_fmtd_air_date = '03-'
        elif 'Apr' in item_air_date: item_fmtd_air_date = '04-'
        elif 'May' in item_air_date: item_fmtd_air_date = '05-'
        elif 'Jun' in item_air_date: item_fmtd_air_date = '06-'
        elif 'Jul' in item_air_date: item_fmtd_air_date = '07-'
        elif 'Aug' in item_air_date: item_fmtd_air_date = '08-'
        elif 'Sep' in item_air_date: item_fmtd_air_date = '09-'
        elif 'Oct' in item_air_date: item_fmtd_air_date = '10-'
        elif 'Nov' in item_air_date: item_fmtd_air_date = '11-'
        elif 'Dec' in item_air_date: item_fmtd_air_date = '12-'
        else: item_fmtd_air_date = '12-'
        date = re.search('([0-9]{1,2})', item_air_date)
        if date: 
            date = date.group(1)
            item_fmtd_air_date += "%02d-" % int(date)
        else:
            item_fmtd_air_date += "01-"
        year = re.search('([0-9]{4})', item_air_date)
        if year: 
            year = year.group(1)
            item_fmtd_air_date += year
        else:
            item_fmtd_air_date += "0001"
            
        try:
            item_fmtd_air_date = datetime.datetime.strptime(item_fmtd_air_date, "%m-%d-%Y")
        except TypeError:
            import time
            item_fmtd_air_date = datetime.datetime(*(time.strptime(item_fmtd_air_date, "%m-%d-%Y")[0:6]))
            
        return item_fmtd_air_date

    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):      
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)

        import re
        
        new_url = url
        if not new_url.startswith(self.get_url()):
            new_url = re.sub("http\://.*?/", self.get_url(), url)
        
        from entertainment.net import Net
        net = Net(cached=False)
        content = net.http_GET(new_url).content

        print 'new_url getcontent ' + new_url
        import datetime
        todays_date = datetime.date.today()

        subscripions_delay_days = self.Settings().get_setting('subscripions_delay_days')
        if subscripions_delay_days != '-':
            todays_date = todays_date + datetime.timedelta(days=-int(subscripions_delay_days))

        if type == 'tv_seasons':
            check_season = 0
            last_season = 0
            season_url = None
            seasons = re.search('<a href="/(title/.+?/episodes\?season=)([0-9]+)', content)
            if seasons:
                last_season = int(seasons.group(2))
                season_url = seasons.group(1)
            
            for season_num in xrange(last_season, 0, -1):
                item_v_id = str(season_num)
                item_url = self.get_url() + season_url + item_v_id
                
                if check_season < 2:
                    check_season += 1
                    item_content = net.http_GET(item_url).content
                    season_item = re.search('<div>S' + item_v_id +', Ep([0-9]+)</div>', item_content)
                    if not season_item: 
                        check_season -= 1
                        continue          
                    item_item = re.search('(?s)<div class="list_item.+?href="(.+?)".+?title="(.+?)".+?<div>S' + item_v_id +', Ep([0-9]+)</div>.+?<div class="airdate">(.+?)</div>', item_content)
                    if 'unknown' in item_item.group(4).lower(): continue 
                    item_fmtd_air_date = self.get_formated_date( item_item.group(4) )

                    if item_fmtd_air_date.date() > todays_date or str(item_fmtd_air_date.date()).split(' ')[0] == '0001-12-01': continue
                
                item_title = 'Season ' + item_v_id
                
                item_id = common.CreateIdFromString(title + ' ' + item_title)
                
                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=item_url, name=name, year=year, season=item_v_id)

        elif type == 'tv_episodes':
            season_item = re.search('<div>S' + season +', Ep([0-9]+)</div>', content)

            if not season_item:
                return

            for item in re.finditer('(?s)<div class="list_item.+?href="(.+?)".+?title="(.+?)".+?<div>S' + season +', Ep([0-9]+)</div>.+?<div class="airdate">(.+?)</div>', content):
                item_fmtd_air_date = self.get_formated_date( item.group(4) )

                if self.Settings().get_setting('future')=='false':
                    if item_fmtd_air_date.date() > todays_date or str(item_fmtd_air_date.date()).split(' ')[0] == '0001-12-01': break

                item_url = self.get_url() + item.group(1)
                item_v_id = item.group(3)
                item_title = item.group(2)
                if item_title == None:
                    item_title = ''
                
                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + season + '_episode_' + item_v_id)
                '''
                print 'presume Addcontent episodes'
                print 'item_indexer ' + str(indexer) + '|item_title ' + item_title + '|item_name ' + name + '|item year ' + year + '|item season ' + season + '|episode ' + str(item_v_id)
                print 'item_url ' + str(item_url)
                print 'item_id ' + str(item_id)
                '''
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, year=year, season=season, episode=item_v_id)

    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        import datetime

        # Get a date object
        todays_date = datetime.date.today()

        user_number = self.Settings().get_setting('imdb_user_number')
        imdb_userlist_number = self.Settings().get_setting('imdb_userlist_number')

        movie_votes_regular = self.Settings().get_setting('movie_votes_regular')
        movie_votes_less = self.Settings().get_setting('movie_votes_less')
        movie_votes_small = self.Settings().get_setting('movie_votes_small')
        movie_votes_language = self.Settings().get_setting('movie_votes_language')
        movie_votes_rated = self.Settings().get_setting('movie_votes_rated')
        movie_votes_rated_language = self.Settings().get_setting('movie_votes_rated_language')
        movie_meter_regular = self.Settings().get_setting('movie_meter_regular')
        movie_meter_less = self.Settings().get_setting('movie_meter_less')
        movie_minimum_boxoffice_gross_us = self.Settings().get_setting('movie_minimum_boxoffice_gross_us')
        now_playing_weeks_us = self.Settings().get_setting('now_playing_weeks_us')

        tvshow_votes_regular = self.Settings().get_setting('tvshow_votes_regular')
        tvshow_votes_less = self.Settings().get_setting('tvshow_votes_less')
        tvshow_votes_small = self.Settings().get_setting('tvshow_votes_small')
        tvshow_votes_language = self.Settings().get_setting('tvshow_votes_language')
        tvshow_votes_rated = self.Settings().get_setting('tvshow_votes_rated')
        tvshow_votes_rated_language = self.Settings().get_setting('tvshow_votes_rated_language')
        tvshow_meter_regular = self.Settings().get_setting('tvshow_meter_regular')
        tvshow_meter_less = self.Settings().get_setting('tvshow_meter_less')
        tvshow_production_status = self.Settings().get_setting('tvshow_production_status')

        search_now_playing_date = todays_date + datetime.timedelta(weeks=-int(now_playing_weeks_us))

        if self.Settings().get_setting('ShowSortByOptions')=='true':
            dict = self.GetSortByOptions()
            movie_GetSortByOptions = ' [' + dict[self.Settings().get_setting('movie_GetSortByOptions')] + ']'
            movie_GetSortByOptions_now_playing_us = ' [' + dict[self.Settings().get_setting('movie_GetSortByOptions_now_playing_us')] + ']'
            movie_GetSortByOptions_language = ' [' + dict[self.Settings().get_setting('movie_GetSortByOptions_language')] + ']'
            movie_GetSortByOptions_tv = ' [' + dict[self.Settings().get_setting('movie_GetSortByOptions_tv')] + ']'
            movie_GetSortByOptions_awards = ' [' + dict[self.Settings().get_setting('movie_GetSortByOptions_awards')] + ']'
            movie_GetSortByOptions_awards_tv = ' [' + dict[self.Settings().get_setting('movie_GetSortByOptions_awards_tv')] + ']'
            movie_GetSortByOptions_imdb_ratings_charts = ' [' + dict[self.Settings().get_setting('movie_GetSortByOptions_imdb_ratings_charts')] + ']'
            movie_GetSortByOptions_imdb_ratings = ' [' + dict[self.Settings().get_setting('movie_GetSortByOptions_imdb_ratings')] + ']'
            movie_GetSortByOptions_imdb_ratings_bottom = ' [' + dict[self.Settings().get_setting('movie_GetSortByOptions_imdb_ratings_bottom')] + ']'

            tvshow_GetSortByOptions = ' [' + dict[self.Settings().get_setting('tvshow_GetSortByOptions')] + ']'
            tvshow_GetSortByOptions_language = ' [' + dict[self.Settings().get_setting('tvshow_GetSortByOptions_language')] + ']'
            tvshow_GetSortByOptions_awards = ' [' + dict[self.Settings().get_setting('tvshow_GetSortByOptions_awards')] + ']'

            watchlist_GetSortByOptions = ' [' + dict[self.Settings().get_setting('watchlist_GetSortByOptions')] + ']'
            userlist_GetSortByOptions = ' [' + dict[self.Settings().get_setting('userlist_GetSortByOptions')] + ']'
            userlist_People_GetSortByOptions = ' [' + dict[self.Settings().get_setting('userlist_People_GetSortByOptions')] + ']'

        else:
            movie_GetSortByOptions = ''
            movie_GetSortByOptions_now_playing_us = ''
            movie_GetSortByOptions_language = ''
            movie_GetSortByOptions_tv = ''
            movie_GetSortByOptions_awards = ''
            movie_GetSortByOptions_awards_tv = ''
            movie_GetSortByOptions_imdb_ratings_charts = ''
            movie_GetSortByOptions_imdb_ratings = ''
            movie_GetSortByOptions_imdb_ratings_bottom = ''

            tvshow_GetSortByOptions = ''
            tvshow_GetSortByOptions_language = ''
            tvshow_GetSortByOptions_awards = ''

            watchlist_GetSortByOptions = ''
            userlist_GetSortByOptions = ''
            userlist_People_GetSortByOptions = ''

        url_default_movie = 'sort=' + self.Settings().get_setting('movie_GetSortByOptions') + ',' + self.Settings().get_setting('movie_GetSortOrderOptions')
        url_default_movie_now_playing_us = 'sort=' + self.Settings().get_setting('movie_GetSortByOptions_now_playing_us') + ',' + self.Settings().get_setting('movie_GetSortOrderOptions_now_playing_us')
        url_default_movie_language = 'sort=' + self.Settings().get_setting('movie_GetSortByOptions_language') + ',' + self.Settings().get_setting('movie_GetSortOrderOptions_language')
        url_default_movie_tv = 'sort=' + self.Settings().get_setting('movie_GetSortByOptions_tv') + ',' + self.Settings().get_setting('movie_GetSortOrderOptions_tv')
        url_default_movie_awards = 'sort=' + self.Settings().get_setting('movie_GetSortByOptions_awards') + ',' + self.Settings().get_setting('movie_GetSortOrderOptions_awards')
        url_default_movie_awards_tv = 'sort=' + self.Settings().get_setting('movie_GetSortByOptions_awards_tv') + ',' + self.Settings().get_setting('movie_GetSortOrderOptions_awards_tv')
        url_default_movie_imdb_ratings_charts = 'sort=' + self.Settings().get_setting('movie_GetSortByOptions_imdb_ratings_charts') + ',' + self.Settings().get_setting('movie_GetSortOrderOptions_imdb_ratings_charts')
        url_default_movie_imdb_ratings = 'sort=' + self.Settings().get_setting('movie_GetSortByOptions_imdb_ratings') + ',' + self.Settings().get_setting('movie_GetSortOrderOptions_imdb_ratings')
        url_default_movie_imdb_ratings_bottom = 'sort=' + self.Settings().get_setting('movie_GetSortByOptions_imdb_ratings_bottom') + ',' + self.Settings().get_setting('movie_GetSortOrderOptions_imdb_ratings_bottom')

        url_default_tvshow = 'sort=' + self.Settings().get_setting('tvshow_GetSortByOptions') + ',' + self.Settings().get_setting('tvshow_GetSortOrderOptions')
        url_default_tvshow_language = 'sort=' + self.Settings().get_setting('tvshow_GetSortByOptions_language') + ',' + self.Settings().get_setting('tvshow_GetSortOrderOptions_language')
        url_default_tvshow_awards = 'sort=' + self.Settings().get_setting('tvshow_GetSortByOptions_awards') + ',' + self.Settings().get_setting('tvshow_GetSortOrderOptions_awards')

        url_default_watchlist = 'sort=' + self.Settings().get_setting('watchlist_GetSortByOptions') + ',' + self.Settings().get_setting('watchlist_GetSortOrderOptions')
        url_default_userlist = 'sort=' + self.Settings().get_setting('userlist_GetSortByOptions') + ',' + self.Settings().get_setting('userlist_GetSortOrderOptions')
        url_default_userlist_people = 'sort=' + self.Settings().get_setting('userlist_People_GetSortByOptions') + ',' + self.Settings().get_setting('userlist_People_GetSortOrderOptions')

        if self.Settings().get_setting('userlist_People_GetSortByOptions') == 'death_date':
            url_default_userlist_people = 'death_date=,' + str(todays_date) + '&' + url_default_userlist_people

        if imdb_userlist_number:
            url_filter_seen = 'lists=!' + imdb_userlist_number + '&'
            url_filter_userlist_seen = ',!' + imdb_userlist_number
        else:
            url_filter_userlist_seen = ''

        url_type_movie = 'title_type=feature,tv_movie,video,tv_special,short&'
        url_type_tvshow = 'title_type=tv_series,mini_series&'
        url_type_watchlist = 'title_type=movie,tvMovie,video,tvSpecial,short,movie,tvSeries,tvMiniSeries&'

        url_filter_movie = 'has=technical&moviemeter=,' + movie_meter_regular + '&num_votes=' + movie_votes_regular + ',&production_status=released&'
        url_filter_rated_movie = 'has=technical&moviemeter=,' + movie_meter_regular + '&num_votes=' + movie_votes_rated + ',&production_status=released&'
        url_filter_boxoffice_movie = 'has=technical&moviemeter=,' + movie_meter_regular + '&num_votes=' + movie_votes_regular + ',&boxoffice_gross_us=' + movie_minimum_boxoffice_gross_us + ',&production_status=released&'
        url_filter_less_movie = 'has=technical&moviemeter=,' + movie_meter_less + '&num_votes=' + movie_votes_less + ',&production_status=released&'
        url_filter_small_movie = 'has=technical&moviemeter=,' + movie_meter_less + '&num_votes=' + movie_votes_small + ',&production_status=released&'
        url_filter_small_boxoffice_movie = 'has=technical&moviemeter=,' + movie_meter_less + '&num_votes=' + movie_votes_small + ',&boxoffice_gross_us=' + movie_minimum_boxoffice_gross_us + ',&production_status=released&'
        url_filter_language_movie = 'has=technical&num_votes=' + movie_votes_language + ',&production_status=released&'
        url_filter_language_rated_movie = 'has=technical&num_votes=' + movie_votes_rated_language + ',&production_status=released&'
        url_filter_language_boxoffice_movie = 'has=technical&num_votes=' + movie_votes_language + ',&boxoffice_gross_us=' + movie_minimum_boxoffice_gross_us + ',&production_status=released&'

        url_filter_tvshow = 'has=technical&moviemeter=,' + tvshow_meter_regular + '&num_votes=' + tvshow_votes_regular + ',&production_status=' + tvshow_production_status + '&'
        url_filter_rated_tvshow = 'has=technical&moviemeter=,' + tvshow_meter_regular + '&num_votes=' + tvshow_votes_rated + ',&production_status=' + tvshow_production_status + '&'
        url_filter_less_tvshow = 'has=technical&moviemeter=,' + tvshow_meter_less + '&num_votes=' + tvshow_votes_less + ',&production_status=' + tvshow_production_status + '&'
        url_filter_small_tvshow = 'has=technical&moviemeter=,' + tvshow_meter_less + '&num_votes=' + tvshow_votes_small + ',&production_status=' + tvshow_production_status + '&'
        url_filter_language_tvshow = 'has=technical&num_votes=' + tvshow_votes_language + ',&production_status=' + tvshow_production_status + '&'
        url_filter_language_rated_tvshow = 'has=technical&num_votes=' + tvshow_votes_rated_language + ',&production_status=' + tvshow_production_status + '&'

        if self.Settings().get_setting('exclude_seen_movies_tvshows')=='true':
            if imdb_userlist_number:
                url_filter_movie = url_filter_seen + url_filter_movie
                url_filter_rated_movie = url_filter_seen + url_filter_rated_movie
                url_filter_boxoffice_movie = url_filter_seen + url_filter_boxoffice_movie
                url_filter_less_movie = url_filter_seen + url_filter_less_movie
                url_filter_small_movie = url_filter_seen + url_filter_small_movie
                url_filter_small_boxoffice_movie = url_filter_seen + url_filter_small_boxoffice_movie
                url_filter_language_movie = url_filter_seen + url_filter_language_movie
                url_filter_language_rated_movie = url_filter_seen + url_filter_language_rated_movie
                url_filter_language_boxoffice_movie = url_filter_seen + url_filter_language_boxoffice_movie

                url_filter_tvshow = url_filter_seen + url_filter_tvshow
                url_filter_rated_tvshow = url_filter_seen + url_filter_rated_tvshow
                url_filter_less_tvshow = url_filter_seen + url_filter_less_tvshow
                url_filter_small_tvshow = url_filter_seen + url_filter_small_tvshow
                url_filter_language_tvshow = url_filter_seen + url_filter_language_tvshow
                url_filter_language_rated_tvshow = url_filter_seen + url_filter_language_rated_tvshow

        if section == 'main':
            if indexer == common.indxr_Movies:
                if self.Settings().get_setting('moviemeter')=='true':
                    self.AddSection(list, indexer, 'moviemeter', 'Most Popular', self.get_url()+'search/title?' + url_filter_movie + url_type_movie + 'sort=moviemeter,asc', indexer)
                if self.Settings().get_setting('boxoffice_gross_us')=='true':
                    self.AddSection(list, indexer, 'boxoffice_gross_us', 'Box Office', self.get_url()+'search/title?' + url_filter_boxoffice_movie + url_type_movie + 'sort=boxoffice_gross_us,desc', indexer)
                if self.Settings().get_setting('genres')=='true':
                    self.AddSection(list, indexer, 'genres', 'Genres' + movie_GetSortByOptions)
                if self.Settings().get_setting('year')=='true':
                    self.AddSection(list, indexer, 'year', 'Year' + movie_GetSortByOptions)
                if self.Settings().get_setting('decade')=='true':
                    self.AddSection(list, indexer, 'decade', 'Decade' + movie_GetSortByOptions)
                if self.Settings().get_setting('now-playing-us')=='true':
                    self.AddSection(list, indexer, 'now-playing-us', 'Now Playing US' + movie_GetSortByOptions_now_playing_us, self.get_url()+'search/title?' + url_filter_small_movie + 'title_type=feature&' + 'groups=now-playing-us&' + 'release_date=' + str(search_now_playing_date) + ',&' + url_default_movie_now_playing_us, indexer)
                if self.Settings().get_setting('user_rating')=='true':
                    self.AddSection(list, indexer, 'user_rating', 'Highly Rated', self.get_url()+'search/title?' + url_filter_rated_movie + url_type_movie + 'sort=user_rating,desc', indexer)
                if self.Settings().get_setting('num_votes')=='true':
                    self.AddSection(list, indexer, 'num_votes', 'Most Voted', self.get_url()+'search/title?' + url_filter_movie + url_type_movie + 'sort=num_votes,desc', indexer)
                if self.Settings().get_setting('additional')=='true':
                    self.AddSection(list, indexer, 'additional', 'Additional')

            elif indexer == common.indxr_TV_Shows:
                if self.Settings().get_setting('moviemeter')=='true':
                    self.AddSection(list, indexer, 'moviemeter', 'Most Popular', self.get_url()+'search/title?' + url_filter_tvshow + url_type_tvshow + 'sort=moviemeter,asc', indexer)
                if self.Settings().get_setting('genres')=='true':
                    self.AddSection(list, indexer, 'genres', 'Genres' + tvshow_GetSortByOptions)
                if self.Settings().get_setting('year')=='true':
                    self.AddSection(list, indexer, 'year', 'Year' + tvshow_GetSortByOptions)
                if self.Settings().get_setting('decade')=='true':
                    self.AddSection(list, indexer, 'decade', 'Decade' + tvshow_GetSortByOptions)
                if self.Settings().get_setting('user_rating')=='true':
                    self.AddSection(list, indexer, 'user_rating', 'Highly Rated', self.get_url()+'search/title?' + url_filter_rated_tvshow + url_type_tvshow + 'sort=user_rating,desc', indexer)
                if self.Settings().get_setting('num_votes')=='true':
                    self.AddSection(list, indexer, 'num_votes', 'Most Voted', self.get_url()+'search/title?' + url_filter_tvshow + url_type_tvshow + 'sort=num_votes,desc', indexer)
                if self.Settings().get_setting('additional')=='true':
                    self.AddSection(list, indexer, 'additional', 'Additional')


            if user_number:
                if self.Settings().get_setting('watch_list_main')=='true':
                    self.AddSection(list, indexer, 'watchlist', 'Watchlist' + watchlist_GetSortByOptions, self.get_url()+'user/' + user_number + '/watchlist?' + url_type_watchlist + 'view=detail' + '&' + url_default_watchlist, indexer)

                    from entertainment.net import Net
                    net = Net(cached=False)
                    import re

                    named_lists_url = self.get_url()+'user/' + user_number + '/lists?tab=public'
                    named_lists = net.http_GET(named_lists_url).content

                    print 'named_lists ' + named_lists.encode('utf-8')

                    match = re.compile('<div class="list_name"><b><a.+?href="(.+?)".+?>(.+?)</a>.+?\n.+?div class="list_meta">(.+?)</div>').findall(named_lists)
                    for url, name ,TYPE in match:
                        custom_name='%s List' % name
                        item_v_id=url.split('/')[2]

                        if 'people' in TYPE:
                            self.AddSection(list, common.indxr_Lists, 'search_gender', '%s' % custom_name + userlist_People_GetSortByOptions, self.get_url()+'search/name?' + 'lists=' + item_v_id + '&' + url_default_userlist_people, indexer, hlevel=1)
                        elif 'episodes' in name:
                            self.AddSection(list, indexer, 'userlist_episodes', '%s' % custom_name + userlist_GetSortByOptions, self.get_url()+'search/title?' + 'lists=' + item_v_id + '&' + url_default_userlist, indexer, hlevel=1)
                        else:
                            self.AddSection(list, indexer, 'userlist', '%s' % custom_name + userlist_GetSortByOptions, self.get_url()+'search/title?' + 'lists=' + item_v_id + url_filter_userlist_seen + '&' + url_default_userlist, indexer, hlevel=1)


        elif section == 'genres_all':#(no filter)*
            if indexer == common.indxr_Movies:
                self.AddSection(list, indexer, 'genres_feature', 'Genres Feature' + movie_GetSortByOptions)
                self.AddSection(list, indexer, 'genres_tv_movie_tv_special', 'Genres TV Movie' + movie_GetSortByOptions_tv)
                self.AddSection(list, indexer, 'genres_video', 'Genres Video' + movie_GetSortByOptions_tv)
                self.AddSection(list, indexer, 'genres_short', 'Genres Short' + movie_GetSortByOptions_tv)


        elif section == 'additional':#(no filter)*
            if indexer == common.indxr_Movies:
                if self.Settings().get_setting('award')=='true':
                    self.AddSection(list, indexer, 'award', 'Awards')
                if self.Settings().get_setting('certificates')=='true':
                    self.AddSection(list, indexer, 'certificates', 'Certificate' + movie_GetSortByOptions)
                if self.Settings().get_setting('company')=='true':
                    self.AddSection(list, indexer, 'company', 'Company' + movie_GetSortByOptions)
                if self.Settings().get_setting('genres_all')=='true':
                    self.AddSection(list, indexer, 'genres_all', 'Genres All')
                if self.Settings().get_setting('imdb_ratings')=='true':
                    self.AddSection(list, indexer, 'imdb_ratings', 'IMDb Ratings')
                if self.Settings().get_setting('imdb_user_picks')=='true':
                    self.AddSection(list, indexer, 'imdb_user_picks', 'IMDb User picks' + movie_GetSortByOptions)
                if self.Settings().get_setting('languages')=='true':
                    self.AddSection(list, indexer, 'languages', 'Language' + movie_GetSortByOptions_language)
                if self.Settings().get_setting('languages_Less-Common')=='true':
                    self.AddSection(list, indexer, 'languages_Less-Common', 'Language Less-Common' + movie_GetSortByOptions_language)
                if self.Settings().get_setting('theaters')=='true':
                    self.AddSection(list, indexer, 'theaters', 'Theaters')
                if self.Settings().get_setting('title_type')=='true':
                    self.AddSection(list, common.indxr_Lists, 'title_type', 'Title Type')
                if self.Settings().get_setting('people')=='true':
                    self.AddSection(list, common.indxr_Lists, 'people', 'People' + userlist_People_GetSortByOptions)
                if self.Settings().get_setting('search_celeb')=='true':
                    self.AddSection(list, common.indxr_Lists, 'search_celeb', 'Search Celebrity', self.get_url()+'find?q=', indexer)
            elif indexer == common.indxr_TV_Shows:
                if self.Settings().get_setting('award')=='true':
                    self.AddSection(list, indexer, 'award', 'Awards')
                if self.Settings().get_setting('imdb_user_picks')=='true':
                    self.AddSection(list, indexer, 'imdb_user_picks', 'IMDb User picks' + tvshow_GetSortByOptions)
                if self.Settings().get_setting('languages')=='true':
                    self.AddSection(list, indexer, 'languages', 'Language' + tvshow_GetSortByOptions_language)
                if self.Settings().get_setting('languages_Less-Common')=='true':
                    self.AddSection(list, indexer, 'languages_Less-Common', 'Language Less-Common' + tvshow_GetSortByOptions_language)

        elif section == 'award':#(no filter)*
            if indexer == common.indxr_Movies:
                self.AddSection(list, indexer, 'award_movies', 'Awards Movies' + movie_GetSortByOptions_awards)
                self.AddSection(list, indexer, 'award_documentary', 'Awards Documentary' + movie_GetSortByOptions_awards_tv)
                self.AddSection(list, indexer, 'award_tv_movies', 'Awards TV Movies' + movie_GetSortByOptions_awards_tv)
                self.AddSection(list, indexer, 'award_shorts', 'Awards Shorts' + movie_GetSortByOptions_awards_tv)
            elif indexer == common.indxr_TV_Shows:
                self.AddSection(list, indexer, 'award_tv_series', 'Awards TV Series' + tvshow_GetSortByOptions_awards)
                self.AddSection(list, indexer, 'award_mini_series', 'Awards Mini-Series' + tvshow_GetSortByOptions_awards)

        elif section == 'award_movies':#(filter_language)*
            if indexer == common.indxr_Movies:
                self.AddSection(list, indexer, 'oscar_best_picture_winners_movies', 'Best Picture Winning', self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=feature&' + 'groups=oscar_best_picture_winners&' + url_default_movie_awards, indexer)
                self.AddSection(list, indexer, 'oscar_winners_movies', 'Oscar-Winning', self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=feature&' + 'groups=oscar_winners&' + url_default_movie_awards, indexer)
                self.AddSection(list, indexer, 'oscar_nominees_movies', 'Oscar-Nominated', self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=feature&' + 'groups=oscar_nominees&' + url_default_movie_awards, indexer)

        elif section == 'award_tv_movies':#(filter_language)*
            if indexer == common.indxr_Movies:
                self.AddSection(list, indexer, 'emmy_winners_tv_movies', 'Emmy Award-Winning', self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=tv_movie&' + 'groups=emmy_winners&' + url_default_movie_awards_tv, indexer)
                self.AddSection(list, indexer, 'emmy_nominees_tv_movies', 'Emmy Award-Nominated', self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=tv_movie&' + 'groups=emmy_nominees&' + url_default_movie_awards_tv, indexer)

        elif section == 'award_shorts':#(filter_language)*
            if indexer == common.indxr_Movies:
                self.AddSection(list, indexer, 'oscar_winners_short', 'Oscar-Winning', self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=short&' + 'groups=oscar_winners&' + url_default_movie_awards_tv, indexer)
                self.AddSection(list, indexer, 'oscar_nominees_short', 'Oscar-Nominated', self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=short&' + 'groups=oscar_nominees&' + url_default_movie_awards_tv, indexer)
                self.AddSection(list, indexer, 'emmy_winners_short', 'Emmy Award-Winning', self.get_url()+'search/title?' + url_filter_language_movie +  'title_type=short&' + 'groups=emmy_winners&' + url_default_movie_awards_tv, indexer)
                self.AddSection(list, indexer, 'emmy_nominees_short', 'Emmy Award-Nominated', self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=short&' + 'groups=emmy_nominees&' + url_default_movie_awards_tv, indexer)

        elif section == 'award_documentary':#(filter_language)*
            if indexer == common.indxr_Movies:
                self.AddSection(list, indexer, 'oscar_winners_documentary', 'Oscar-Winning', self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=documentary&' + 'groups=oscar_winners&' + url_default_movie_awards_tv, indexer)
                self.AddSection(list, indexer, 'oscar_nominees_documentary', 'Oscar-Nominated', self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=documentary&' + 'groups=oscar_nominees&' + url_default_movie_awards_tv, indexer)
                self.AddSection(list, indexer, 'emmy_winners_documentary', 'Emmy Award-Winning', self.get_url()+'search/title?' + url_filter_language_movie +  'title_type=documentary&' + 'groups=emmy_winners&' + url_default_movie_awards_tv, indexer)
                self.AddSection(list, indexer, 'emmy_nominees_documentary', 'Emmy Award-Nominated', self.get_url()+'search/title?' + url_filter_language_movie +  'title_type=documentary&' + 'groups=emmy_nominees&' + url_default_movie_awards_tv, indexer)

        elif section == 'award_tv_series':#(filter_language)*
            if indexer == common.indxr_TV_Shows:
                self.AddSection(list, indexer, 'emmy_winners_tv_shows', 'Emmy Award-Winning', self.get_url()+'search/title?' + url_filter_language_tvshow +  'title_type=tv_series&' + 'groups=emmy_winners&' + url_default_tvshow_awards, indexer)
                self.AddSection(list, indexer, 'emmy_nominees_tv_shows', 'Emmy Award-Nominated', self.get_url()+'search/title?' + url_filter_language_tvshow +  'title_type=tv_series&' + 'groups=emmy_nominees&' + url_default_tvshow_awards, indexer)

        elif section == 'award_mini_series':#(filter_language)*
            if indexer == common.indxr_TV_Shows:
                self.AddSection(list, indexer, 'emmy_winners_tv_shows', 'Emmy Award-Winning', self.get_url()+'search/title?' + url_filter_language_tvshow +  'title_type=mini_series&' + 'groups=emmy_winners&' + url_default_tvshow_awards, indexer)
                self.AddSection(list, indexer, 'emmy_nominees_tv_shows', 'Emmy Award-Nominated', self.get_url()+'search/title?' + url_filter_language_tvshow +  'title_type=mini_series&' + 'groups=emmy_nominees&' + url_default_tvshow_awards, indexer)

        elif section == 'title_type':#(filter_small, filter_language)
            if indexer == common.indxr_Lists:
                self.AddSection(list, indexer, 'feature', 'Feature Movies' + movie_GetSortByOptions, self.get_url()+'search/title?' + url_filter_small_movie + 'title_type=feature&', indexer)
                self.AddSection(list, indexer, 'documentary', 'Documentary Movies' + movie_GetSortByOptions_tv, self.get_url()+'search/title?' + url_filter_small_movie + 'title_type=documentary&' + url_default_movie_tv, indexer)
                sort_by = self.Settings().get_setting('movie_GetSortByOptions_tv')
                if sort_by == 'user_rating':
                    self.AddSection(list, indexer, 'tv_movie', 'TV Movies' + movie_GetSortByOptions_tv, self.get_url()+'search/title?' + url_filter_language_rated_movie + 'title_type=tv_movie&' + url_default_movie_tv, indexer)
                    self.AddSection(list, indexer, 'short', 'Short Movies' + movie_GetSortByOptions_tv, self.get_url()+'search/title?' + url_filter_language_rated_movie + 'title_type=short&' + url_default_movie_tv, indexer)
                    self.AddSection(list, indexer, 'video', 'Videos' + movie_GetSortByOptions_tv, self.get_url()+'search/title?' + url_filter_language_rated_movie + 'title_type=video&' + url_default_movie_tv, indexer)
                    self.AddSection(list, indexer, 'tv_special', 'TV Special' + movie_GetSortByOptions_tv, self.get_url()+'search/title?' + url_filter_language_rated_movie + 'title_type=tv_special&' + url_default_movie_tv, indexer)
                else:
                    self.AddSection(list, indexer, 'tv_movie', 'TV Movies' + movie_GetSortByOptions_tv, self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=tv_movie&' + url_default_movie_tv, indexer)
                    self.AddSection(list, indexer, 'short', 'Short Movies' + movie_GetSortByOptions_tv, self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=short&' + url_default_movie_tv, indexer)
                    self.AddSection(list, indexer, 'video', 'Videos' + movie_GetSortByOptions_tv, self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=video&' + url_default_movie_tv, indexer)
                    self.AddSection(list, indexer, 'tv_special', 'TV Special' + movie_GetSortByOptions_tv, self.get_url()+'search/title?' + url_filter_language_movie + 'title_type=tv_special&' + url_default_movie_tv, indexer)
                self.AddSection(list, indexer, 'tv_series', 'TV Series' + tvshow_GetSortByOptions, self.get_url()+'search/title?' + url_filter_small_tvshow + 'title_type=tv_series&' + url_default_tvshow, indexer)
                self.AddSection(list, indexer, 'mini_series', 'Mini-Series' + tvshow_GetSortByOptions, self.get_url()+'search/title?' + url_filter_small_tvshow + 'title_type=mini_series&' + url_default_tvshow, indexer)
                self.AddSection(list, indexer, 'documentary', 'Documentary-Series' + tvshow_GetSortByOptions, self.get_url()+'search/title?' + url_filter_small_tvshow + 'title_type=tv_series,mini_series&genres=documentary&' + url_default_tvshow, indexer)

        elif section == 'company':#(filter_language)*
            if indexer == common.indxr_Movies:
                self.AddSection(list, indexer, 'fox', '20th Century Fox', self.get_url()+'search/title?' + url_filter_language_movie + 'companies=fox&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'dreamworks', 'DreamWorks', self.get_url()+'search/title?' + url_filter_language_movie + 'companies=dreamworks&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'mgm', 'MGM', self.get_url()+'search/title?' + url_filter_language_movie + 'companies=mgm&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'paramount', 'Paramount', self.get_url()+'search/title?' + url_filter_language_movie + 'companies=paramount&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'columbia', 'Sony', self.get_url()+'search/title?' + url_filter_language_movie + 'companies=columbia&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'universal', 'Universal', self.get_url()+'search/title?' + url_filter_language_movie + 'companies=universal&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'disney', 'Walt Disney', self.get_url()+'search/title?' + url_filter_language_movie + 'companies=disney&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'warner', 'Warner Bros.', self.get_url()+'search/title?' + url_filter_language_movie + 'companies=warner&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'amazon_paid', 'Amazon Instant Video US', self.get_url()+'search/title?' + url_filter_language_movie + 'online_availability=US/today/Amazon/paid,US/today/Amazon/subs&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'amazon_prime', 'Amazon Prime Instant Video US', self.get_url()+'search/title?' + url_filter_language_movie + 'online_availability=US/today/Amazon/subs&' + url_type_movie, indexer)

        elif section == 'certificates':#(filter_small)*
            if indexer == common.indxr_Movies:
                self.AddSection(list, indexer, 'kids', 'Kids Zone', self.get_url()+'search/title?' + url_filter_small_movie + 'certificates=us:g&genres=family&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'certificate_g', 'G', self.get_url()+'search/title?' + url_filter_small_movie + 'certificates=us:g&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'certificate_pg', 'PG', self.get_url()+'search/title?' + url_filter_small_movie + 'certificates=us:pg&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'certificate_pg-13', 'PG-13', self.get_url()+'search/title?' + url_filter_small_movie + 'certificates=us:pg_13&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'certificate_rated', 'Rated', self.get_url()+'search/title?' + url_filter_small_movie + 'certificates=us:r&' + url_type_movie, indexer)
                self.AddSection(list, indexer, 'certificate_nc-17', 'NC-17', self.get_url()+'search/title?' + url_filter_small_movie + 'certificates=us:nc_17&' + url_type_movie, indexer)

        elif section == 'decade':#(filter_small)*
            if indexer == common.indxr_Movies:
                self.AddSection(list, indexer, '2010s', '2010-2015', self.get_url()+'search/title?' +'release_date=2010,2015&' + url_filter_less_movie + url_type_movie, indexer)
                self.AddSection(list, indexer, '2000s', '2000-2009', self.get_url()+'search/title?' +'release_date=2000,2009&' + url_filter_less_movie + url_type_movie, indexer)
                self.AddSection(list, indexer, '1990s', '1990-1999', self.get_url()+'search/title?' +'release_date=1990,1999&' + url_filter_less_movie + url_type_movie, indexer)
                self.AddSection(list, indexer, '1980s', '1980-1989', self.get_url()+'search/title?' +'release_date=1980,1989&' + url_filter_small_movie + url_type_movie, indexer)
                self.AddSection(list, indexer, '1970s', '1970-1979', self.get_url()+'search/title?' +'release_date=1970,1979&' + url_filter_small_movie + url_type_movie, indexer)
                self.AddSection(list, indexer, '1960s', '1960-1969', self.get_url()+'search/title?' +'release_date=1960,1969&' + url_filter_small_movie + url_type_movie, indexer)
                self.AddSection(list, indexer, '1950s', '1950-1959', self.get_url()+'search/title?' +'release_date=1950,1959&' + url_filter_small_movie + url_type_movie, indexer)
                self.AddSection(list, indexer, '1940s', '1940-1949', self.get_url()+'search/title?' +'release_date=1940,1949&' + url_filter_small_movie + url_type_movie, indexer)
                self.AddSection(list, indexer, '1930s', '1930-1939', self.get_url()+'search/title?' +'release_date=1930,1939&' + url_filter_small_movie + url_type_movie, indexer)
                self.AddSection(list, indexer, '1900-20s', '1900-1929', self.get_url()+'search/title?' +'release_date=1900,1929&' + url_filter_small_movie + url_type_movie, indexer)
            elif indexer == common.indxr_TV_Shows:
                self.AddSection(list, indexer, '2010s', '2010-2015', self.get_url()+'search/title?' +'release_date=2010,2015&' + url_filter_less_tvshow + url_type_tvshow, indexer)
                self.AddSection(list, indexer, '2000s', '2000-2009', self.get_url()+'search/title?' +'release_date=2000,2009&' + url_filter_less_tvshow + url_type_tvshow, indexer)
                self.AddSection(list, indexer, '1990s', '1990-1999', self.get_url()+'search/title?' +'release_date=1990,1999&' + url_filter_small_tvshow + url_type_tvshow, indexer)
                self.AddSection(list, indexer, '1980s', '1980-1989', self.get_url()+'search/title?' +'release_date=1980,1989&' + url_filter_small_tvshow + url_type_tvshow, indexer)
                self.AddSection(list, indexer, '1970s', '1970-1979', self.get_url()+'search/title?' +'release_date=1970,1979&' + url_filter_small_tvshow + url_type_tvshow, indexer)
                self.AddSection(list, indexer, '1950-60s', '1949-1969', self.get_url()+'search/title?' +'release_date=1949,1969&' + url_filter_small_tvshow + url_type_tvshow, indexer)

        elif section == 'year':#(filter_small)*
            if indexer == common.indxr_Movies:
                start = 1930
                if self.Settings().get_setting('movie_GetSortByOptions') == 'boxoffice_gross_us':
                    start = 1960
            elif indexer == common.indxr_TV_Shows:
                start = 1949
            import datetime
            end = datetime.datetime.today().year
            year = []
            for yr in range(end, start-1, -1):
                str_year = str(yr)
                if indexer == common.indxr_Movies:
                    self.AddSection(list, indexer, str_year, str_year, self.get_url()+'search/title?' + url_filter_small_movie + 'year=' + str_year+','+str_year + '&' + url_type_movie, indexer)
                elif indexer == common.indxr_TV_Shows:
                    self.AddSection(list, indexer, str_year, str_year, self.get_url()+'search/title?' + url_filter_small_tvshow + 'year=' + str_year+','+str_year + '&' + url_type_tvshow, indexer)

        elif section in ['genres','genres_feature','genres_tv_movie_tv_special','genres_video','genres_short']:#(filter_small)*

            import re
            from entertainment.net import Net
            net = Net()
            
            genre_url = self.get_url()         
            genre_re = ''
            genre_url = genre_url + 'genre/'

            if indexer == common.indxr_Movies:
                if section == 'genres':
                    url_type_movie_genre = 'title_type=feature,tv_movie,tv_special,video,short&'
                    url_default_genres = url_default_movie
                elif section == 'genres_feature':
                    url_type_movie_genre = 'title_type=feature&'
                    url_default_genres = url_default_movie
                elif section == 'genres_tv_movie_tv_special':
                    url_type_movie_genre = 'title_type=tv_movie,tv_special&'
                    url_default_genres = url_default_movie_tv
                elif section == 'genres_video':
                    url_type_movie_genre = 'title_type=video&'
                    url_default_genres = url_default_movie_tv
                elif section == 'genres_short':
                    url_type_movie_genre = 'title_type=short&'
                    url_default_genres = url_default_movie_tv
            elif indexer == common.indxr_TV_Shows:
                if section == 'genres':
                    url_type_tvshow_genre = 'title_type=tv_series,mini_series&'
                    url_default_genres = url_default_tvshow

            if indexer == common.indxr_Movies or indexer == common.indxr_Lists:
                genre_re = '(?s)<h2>On Amazon Prime Instant Video.+?<table(.+?)</table>'
            elif indexer == common.indxr_TV_Shows:
                genre_re = '(?s)<h2>Television.+?<table(.+?)</table>'

            content = net.http_GET(genre_url).content
            genres = re.search(genre_re, content)
            if genres:
                genres = genres.group(1)

                for genre in re.finditer('<a href=".+?">(.+?)</a>', genres):
                    genre_title = genre.group(1)
                    genre_section = genre_title.lower()

                    #added filter for movies and tv shows
                    #solved - sign problem in url
                    #request: some of the genres are empty, empty genres shouldn't be visible, by example game-show for movies.
                    genre_section = genre_section.replace("-", "_")

                    if indexer == common.indxr_Movies:
                        genre_url = self.get_url()+'search/title?' + url_filter_small_movie + url_type_movie_genre + 'genres=' + genre_section
                        genre_url_no_type = self.get_url()+'search/title?' + url_filter_small_movie + 'genres=' + genre_section
                    elif indexer == common.indxr_TV_Shows:
                        genre_url = self.get_url()+'search/title?' + url_filter_small_tvshow + url_type_tvshow_genre + 'genres=' + genre_section
                        genre_url_no_type = self.get_url()+'search/title?' + url_filter_small_tvshow + 'genres=' + genre_section
                        if genre_section == 'sitcom':
                            genre_url = self.get_url()+'search/title?' + url_filter_small_tvshow + url_type_tvshow_genre + 'keywords=sitcom&' + 'genres=' + 'comedy'
                            genre_url_no_type = self.get_url()+'search/title?' + url_filter_small_tvshow + 'keywords=sitcom&' + 'genres=' + 'comedy'

                    #genres for movies and tv shows:
                    if genre_section == 'action':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_short']:
                            self.AddSection(list, indexer, genre_section + '_crime_adventure', genre_title + ' Crime & Adventure', genre_url + ',crime,adventure&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_thriller', genre_title + ' Thriller', genre_url + ',thriller&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_short']:
                            self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'adventure':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        if indexer == common.indxr_Movies:
                            if section not in ['genres_video','genres_short']:
                                self.AddSection(list, indexer, genre_section + '_biography', genre_title + ' Biography', genre_url + ',biography&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_thriller', genre_title + ' Thriller', genre_url + ',thriller&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'animation':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_family', genre_title + ' Family', genre_url + ',family&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_fantasy', genre_title + ' Fantasy', genre_url + ',fantasy&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'biography':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        if indexer == common.indxr_Movies:
                            if section not in ['genres_video','genres_short']:
                                self.AddSection(list, indexer, genre_section + '_crime', genre_title + ' Crime', genre_url + ',crime&' + url_default_genres, indexer, hlevel=1)
                            if section not in ['genres_tv_movie_tv_special','genres_video','genres_short']:
                                self.AddSection(list, indexer, genre_section + '_mystery', genre_title + ' Mystery', genre_url + ',mystery&' + url_default_genres, indexer, hlevel=1)
                            if section not in ['genres_video','genres_short']:
                                self.AddSection(list, indexer, genre_section + '_sport', genre_title + ' Sport', genre_url + ',sport&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'comedy':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_action', genre_title + ' Action', genre_url + ',action&' + url_default_genres, indexer, hlevel=1)
                        if indexer == common.indxr_Movies:
                            if section not in ['genres_tv_movie_tv_special','genres_short']:
                                self.AddSection(list, indexer, genre_section + '_erotica', genre_title + ' Erotica', genre_url + '&' + 'keywords=erotica&' + url_default_genres, indexer, hlevel=1)#
                        self.AddSection(list, indexer, genre_section + '_horror', genre_title + ' Horror', genre_url + ',horror&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_romance', genre_title + ' Romance', genre_url + ',romance&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_tv_movie_tv_special','genres_video']:
                            self.AddSection(list, indexer, genre_section + '_slapstick', genre_title + ' Slapstick', genre_url + '&' + 'keywords=slapstick&' + url_default_genres, indexer, hlevel=1)#
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'crime':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_action_adventure', genre_title + ' Action & Adventure', genre_url + 'action,adventure&' + url_default_genres, indexer, hlevel=1)#
                        self.AddSection(list, indexer, genre_section + '_drama', genre_title + ' Drama', genre_url + ',drama&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_tv_movie_tv_special','genres_video','genres_short']:
                            self.AddSection(list, indexer, genre_section + '_femme-fatale', genre_title + ' Femme Fatale', genre_url + '&' + 'keywords=femme-fatale&' + url_default_genres, indexer, hlevel=1)#
                        if section not in ['genres_short']:
                            self.AddSection(list, indexer, genre_section + '_mystery', genre_title + ' Mystery', genre_url + ',mystery&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_video','genres_short']:
                            self.AddSection(list, indexer, genre_section + '_romance', genre_title + ' Romance', genre_url + ',romance&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'drama':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        if section not in ['genres_video','genres_short']:
                            self.AddSection(list, indexer, genre_section + '_based-on-book', genre_title + ' Based On Book', genre_url + '&' + 'keywords=based-on-book&' + url_default_genres, indexer, hlevel=1)#
                        if indexer == common.indxr_Movies:
                            if section not in ['genres_video','genres_short']:
                                self.AddSection(list, indexer, genre_section + '_erotica', genre_title + ' Erotica', genre_url + '&' + 'keywords=erotica&' + url_default_genres, indexer, hlevel=1)#
                        self.AddSection(list, indexer, genre_section + '_romance', genre_title + ' Romance', genre_url + ',romance&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_short']:
                            self.AddSection(list, indexer, genre_section + '_musical', genre_title + ' Musical', genre_url + ',musical&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_tv_movie_tv_special','genres_video','genres_short']:
                            self.AddSection(list, indexer, genre_section + '_supernatural', genre_title + ' Supernatural', genre_url + '&' + 'keywords=supernatural&' + url_default_genres, indexer, hlevel=1)#
                        if section not in ['genres_video']:
                            self.AddSection(list, indexer, genre_section + '_war', genre_title + ' War', genre_url + ',war&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'family':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_adventure', genre_title + ' Adventure', genre_url + ',adventure&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        if indexer == common.indxr_Movies:
                            self.AddSection(list, indexer, genre_section + '_disney', genre_title + ' Walt Disney', genre_url + '&' + 'companies=disney&' + url_default_genres, indexer, hlevel=1)#
                        self.AddSection(list, indexer, genre_section + '_fantasy', genre_title + ' Fantasy', genre_url + ',fantasy&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_romance', genre_title + ' Romance', genre_url + ',romance&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'fantasy':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_adventure', genre_title + ' Adventure', genre_url + ',adventure&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_drama', genre_title + ' Drama', genre_url + ',drama&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_romance', genre_title + ' Romance', genre_url + ',romance&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'film_noir':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        if section not in ['genres_tv_movie_tv_special','genres_video','genres_short']:#(filter_small)*
                            self.AddSection(list, indexer, genre_section + '_crime', genre_title + ' Crime', genre_url + ',crime&' + url_default_genres, indexer, hlevel=1)
                            self.AddSection(list, indexer, genre_section + '_mystery', genre_title + ' Mystery', genre_url + ',mystery&' + url_default_genres, indexer, hlevel=1)
                            self.AddSection(list, indexer, genre_section + '_romance', genre_title + ' Romance', genre_url + ',romance&' + url_default_genres, indexer, hlevel=1)
                            self.AddSection(list, indexer, genre_section + '_thriller', genre_title + ' Thriller', genre_url + ',thriller&' + url_default_genres, indexer, hlevel=1)
                            self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'history':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        if section not in ['genres_video','genres_short']:
                            self.AddSection(list, indexer, genre_section + '_adventure', genre_title + ' Adventure', genre_url + ',adventure&' + url_default_genres, indexer, hlevel=1)
                            self.AddSection(list, indexer, genre_section + '_biography', genre_title + ' Biography', genre_url + ',biography&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_video']:
                            self.AddSection(list, indexer, genre_section + '_drama', genre_title + ' Drama', genre_url + ',drama&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_video','genres_short']:
                            self.AddSection(list, indexer, genre_section + '_war', genre_title + ' War', genre_url + ',war&' + url_default_genres, indexer, hlevel=1)
                            self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'horror':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_short']:
                            self.AddSection(list, indexer, genre_section + '_drama', genre_title + ' Drama', genre_url + ',drama&' + url_default_genres, indexer, hlevel=1)
                        if indexer == common.indxr_Movies:
                            if section not in ['genres_tv_movie_tv_special','genres_video','genres_short']:
                                self.AddSection(list, indexer, genre_section + '_erotica', genre_title + ' Erotica', genre_url + '&' + 'keywords=erotica&' + url_default_genres, indexer, hlevel=1)#
                        if section not in ['genres_short']:
                            self.AddSection(list, indexer, genre_section + '_gore', genre_title + ' Gore', genre_url + '&' + 'keywords=gore&' + url_default_genres, indexer, hlevel=1)#
                            self.AddSection(list, indexer, genre_section + '_sci_fi', genre_title + ' Sci-Fi', genre_url + ',sci_fi&' + url_default_genres, indexer, hlevel=1)
                            self.AddSection(list, indexer, genre_section + '_serial-killer', genre_title + ' Serial Killer', genre_url + '&' + 'keywords=serial-killer&' + url_default_genres, indexer, hlevel=1)#
                        if indexer == common.indxr_Movies:
                            if section not in ['genres_tv_movie_tv_special','genres_short']:
                                self.AddSection(list, indexer, genre_section + '_slasher', genre_title + ' Slasher', genre_url + '&' + 'keywords=slasher&' + url_default_genres, indexer, hlevel=1)#
                        if section not in ['genres_short']:
                            self.AddSection(list, indexer, genre_section + '_supernatural', genre_title + ' Supernatural', genre_url + '&' + 'keywords=supernatural&' + url_default_genres, indexer, hlevel=1)#
                        if section not in ['genres_short']:
                            self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'music':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        if indexer == common.indxr_Movies:
                            if section not in ['genres_video','genres_short']:
                                self.AddSection(list, indexer, genre_section + '_biography', genre_title + ' Biography', genre_url + ',biography&' + url_default_genres, indexer, hlevel=1)
                            if section == 'genres':
                                self.AddSection(list, indexer, genre_section + '_documentary', genre_title + ' Documentary', genre_url_no_type + ',documentary&' + 'title_type=documentary&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_short']:
                            self.AddSection(list, indexer, genre_section + '_drama', genre_title + ' Drama', genre_url + ',drama&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'musical':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        if indexer == common.indxr_Movies:
                            if section not in ['genres_tv_movie_tv_special','genres_video','genres_short']:
                                self.AddSection(list, indexer, genre_section + '_mystery', genre_title + ' Mystery', genre_url + ',mystery&' + url_default_genres, indexer, hlevel=1)
                            if section not in ['genres_short']:
                                self.AddSection(list, indexer, genre_section + '_romance', genre_title + ' Romance', genre_url + ',romance&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'mystery':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        if section not in ['genres_video','genres_short']:
                            self.AddSection(list, indexer, genre_section + '_adventure', genre_title + ' Adventure', genre_url + ',adventure&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_short']:
                            self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                            self.AddSection(list, indexer, genre_section + '_thriller', genre_title + ' Thriller', genre_url + ',thriller&' + url_default_genres, indexer, hlevel=1)
                            self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'romance':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_video','genres_short']:
                            self.AddSection(list, indexer, genre_section + '_crime', genre_title + ' Crime', genre_url + ',crime&' + url_default_genres, indexer, hlevel=1)
                            self.AddSection(list, indexer, genre_section + '_mystery', genre_title + ' Mystery', genre_url + ',mystery&' + url_default_genres, indexer, hlevel=1)
                            self.AddSection(list, indexer, genre_section + '_thriller', genre_title + ' Thriller', genre_url + ',thriller&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'sci_fi':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_action_fantasy', genre_title + ' Action & Fantasy', genre_url + ',action,fantasy&' + url_default_genres, indexer, hlevel=1)#
                        self.AddSection(list, indexer, genre_section + '_animation', genre_title + ' Animation', genre_url + ',animation&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_short']:
                            self.AddSection(list, indexer, genre_section + '_horror', genre_title + ' Horror', genre_url + ',horror&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_tv_movie_tv_special','genres_video','genres_short']:
                            self.AddSection(list, indexer, genre_section + '_supernatural', genre_title + ' Supernatural', genre_url + '&' + 'keywords=supernatural&' + url_default_genres, indexer, hlevel=1)#
                        self.AddSection(list, indexer, genre_section + '_thriller', genre_title + ' Thriller', genre_url + ',thriller&' + url_default_genres, indexer, hlevel=1)#
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'sport':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        if indexer == common.indxr_Movies:
                            if section not in ['genres_video','genres_short']:
                                self.AddSection(list, indexer, genre_section + '_biography', genre_title + ' Biography', genre_url + ',biography&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        if indexer == common.indxr_Movies:
                            if section == 'genres':
                                self.AddSection(list, indexer, genre_section + '_documentary', genre_title + ' Documentary', genre_url_no_type + ',documentary&' + 'title_type=documentary&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_short']:
                            self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'thriller':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        if section not in ['genres_short']:
                            self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                            self.AddSection(list, indexer, genre_section + '_crime', genre_title + ' Crime', genre_url + ',crime&' + url_default_genres, indexer, hlevel=1)
                        if indexer == common.indxr_Movies:
                            if section not in ['genres_tv_movie_tv_special','genres_short']:
                                self.AddSection(list, indexer, genre_section + '_erotica', genre_title + ' Erotica', genre_url + '&' + 'keywords=erotica&' + url_default_genres, indexer, hlevel=1)#
                        if section not in ['genres_short']:
                            self.AddSection(list, indexer, genre_section + '_horror', genre_title + ' Horror', genre_url + ',horror&' + url_default_genres, indexer, hlevel=1)
                            self.AddSection(list, indexer, genre_section + '_mystery', genre_title + ' Mystery', genre_url + ',mystery&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_sci_fi', genre_title + ' Sci-Fi', genre_url + ',sci_fi&' + url_default_genres, indexer, hlevel=1)#
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'war':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        if section not in ['genres_short']:
                            self.AddSection(list, indexer, genre_section + '_action', genre_title + ' Action', genre_url + ',action&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_video','genres_short']:
                            self.AddSection(list, indexer, genre_section + '_biography', genre_title + ' Biography', genre_url + ',biography&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_tv_movie_tv_special','genres_video']:
                            self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        if indexer == common.indxr_Movies:
                            if section == 'genres':
                                self.AddSection(list, indexer, genre_section + '_documentary', genre_title + ' Documentary', genre_url_no_type + ',documentary&' + 'title_type=documentary&' + url_default_genres, indexer, hlevel=1)
                        elif indexer == common.indxr_TV_Shows:
                            if section == 'genres':
                                self.AddSection(list, indexer, genre_section + '_documentary', genre_title + ' Documentary', genre_url + ',documentary&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'western':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        if section not in ['genres_video','genres_short']:
                            self.AddSection(list, indexer, genre_section + '_action', genre_title + ' Action', genre_url + ',action&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_tv_movie_tv_special']:
                            self.AddSection(list, indexer, genre_section + '_adventure', genre_title + ' Adventure', genre_url + ',adventure&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_tv_movie_tv_special','genres_video']:
                            self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        if section not in ['genres_short']:
                            self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    #genres with a different title type for movies and tw shows.
                    elif genre_section == 'documentary':
                        if section == 'genres':
                            if indexer == common.indxr_Movies:
                                self.AddSection(list, indexer, genre_section, genre_title, genre_url_no_type + '&' + 'title_type=documentary&' + url_default_genres, indexer)
                                self.AddSection(list, indexer, genre_section + '_biography', genre_title + ' Biography', genre_url_no_type + ',biography&' + 'title_type=documentary&' + url_default_genres, indexer, hlevel=1)
                                self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url_no_type + ',comedy&' + 'title_type=documentary&' + url_default_genres, indexer, hlevel=1)
                                self.AddSection(list, indexer, genre_section + '_crime', genre_title + ' Crime', genre_url_no_type + ',crime&' + 'title_type=documentary&' + url_default_genres, indexer, hlevel=1)
                                self.AddSection(list, indexer, genre_section + '_history', genre_title + ' History', genre_url_no_type + ',history&' + 'title_type=documentary&' + url_default_genres, indexer, hlevel=1)
                                self.AddSection(list, indexer, genre_section + '_nature', genre_title + ' Nature', genre_url_no_type + '&' + 'title_type=documentary&' + 'keywords=nature&' + url_default_genres, indexer, hlevel=1)#
                                self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)
                            elif indexer == common.indxr_TV_Shows:
                                self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                                self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                                self.AddSection(list, indexer, genre_section + '_history', genre_title + ' History', genre_url + ',history&' + url_default_genres, indexer, hlevel=1)
                                self.AddSection(list, indexer, genre_section + '_nature', genre_title + ' Nature', genre_url + '&' + 'keywords=nature&' + url_default_genres, indexer, hlevel=1)#
                                self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    #genres for tv shows, not in movies:
                    elif genre_section == 'game_show':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_family', genre_title + ' Family', genre_url + ',family&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_reality_tv', genre_title + ' Reality TV', genre_url + ',reality_tv&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'news':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        if indexer == common.indxr_Movies:
                            self.AddSection(list, indexer, genre_section + '_documentary', genre_title + ' Documentary', genre_url + ',documentary&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_talk_show', genre_title + ' Talk Show', genre_url + ',talk_show&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'reality_tv':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_documentary', genre_title + ' Documentary', genre_url + ',documentary&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_game_show', genre_title + ' Game Show', genre_url + ',game_show&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'sitcom':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_family', genre_title + ' Family', genre_url + ',family&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_romance', genre_title + ' Romance', genre_url + ',romance&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)

                    elif genre_section == 'talk_show':
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)
                        self.AddSection(list, indexer, genre_section + '_comedy', genre_title + ' Comedy', genre_url + ',comedy&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_music', genre_title + ' Music', genre_url + ',music&' + url_default_genres, indexer, hlevel=1)
                        self.AddSection(list, indexer, genre_section + '_news', genre_title + ' News', genre_url + ',news&' + url_default_genres, indexer, hlevel=1)
                        self.get_sub_genres(indexer, section, genre_section,  genre_url_no_type, genre_title, list)
                    else:
                        self.AddSection(list, indexer, genre_section, genre_title, genre_url + '&' + url_default_genres, indexer)

        elif section == 'imdb_ratings':#(no filter, filter_language)*
            if indexer == common.indxr_Movies:
                if self.Settings().get_setting('imdb_ratings_imdb_top_250')=='true':
                    self.AddSection(list, indexer, 'imdbcharts', 'IMDb Top 250' + movie_GetSortByOptions_imdb_ratings_charts, self.get_url()+'chart/top?' + url_default_movie_imdb_ratings_charts, indexer)
                self.AddSection(list, indexer, 'top_1000', 'IMDb Top 1000' + movie_GetSortByOptions_imdb_ratings, self.get_url()+'search/title?' + url_filter_language_movie + url_type_movie + 'groups==top_1000&' + url_default_movie_imdb_ratings, indexer)
                self.AddSection(list, indexer, 'bottom_1000', 'IMDb Bottom 1000' + movie_GetSortByOptions_imdb_ratings_bottom, self.get_url()+'search/title?' + url_filter_language_movie + url_type_movie + 'groups==bottom_1000&' + url_default_movie_imdb_ratings_bottom, indexer)

        elif section == 'imdb_user_picks':#(no filter)*
            if indexer == common.indxr_Movies:
                self.AddSection(list, indexer, 'userlist', '100 GREATEST MOVIES OF ALL TIME: EPISODE I', self.get_url()+'search/title?' + 'lists=ls075131616' + url_filter_userlist_seen + '&' + url_default_movie, indexer)
                self.AddSection(list, indexer, 'userlist', '100 GREATEST MOVIES OF ALL TIME: EPISODE II', self.get_url()+'search/title?' + 'lists=ls075185529' + url_filter_userlist_seen + '&' + url_default_movie, indexer)
                self.AddSection(list, indexer, 'userlist', '100 GREATEST MOVIES OF ALL TIME: EPISODE III', self.get_url()+'search/title?' + 'lists=ls075182307' + url_filter_userlist_seen + '&' + url_default_movie, indexer)
                self.AddSection(list, indexer, 'userlist', 'American Movies of the last 100 years', self.get_url()+'search/title?' + 'lists=ls000050207' + url_filter_userlist_seen + '&' + url_default_movie, indexer)
            elif indexer == common.indxr_TV_Shows:
                self.AddSection(list, indexer, 'userlist', 'Top TV Shows of 2014', self.get_url()+'search/title?' + 'lists=ls071831623' + url_filter_userlist_seen + '&' + url_default_tvshow, indexer)
                self.AddSection(list, indexer, 'userlist', 'On TV: Shows That Are Ending', self.get_url()+'search/title?' + 'lists=ls073546576' + url_filter_userlist_seen + '&' + url_default_tvshow, indexer)

        elif section in ['languages','languages_Less-Common']:#(filter_language)*

            import re
            from entertainment.net import Net
            net = Net()
            language_url = self.get_url() + 'language/'

            if section == 'languages':
                language_re = '(?s)<h2>Common Languages.+?<table(.+?)</table>'
            else:
                language_re = '(?s)<h2>Less-Common Languages.+?<table(.+?)</table>'

            if self.Settings().get_setting('en_us')=='true':
                content = net.http_GET(language_url,{'Accept-Language':'en-US'}).content
            else:
                content = net.http_GET(language_url).content

            languages = re.search(language_re, content)
            if languages:
                languages = languages.group(1)
                for language in re.finditer('<a href="/language/(.+?)">(.+?)</a>', languages):
                    language_title = language.group(2)
                    language_section = language.group(1).lower()

                    if indexer == common.indxr_Movies:
                        sort_by = self.Settings().get_setting('movie_GetSortByOptions_language')
                        if sort_by == 'boxoffice_gross_us':
                            language_url = self.get_url() + 'search/title?' + url_filter_language_boxoffice_movie + url_type_movie + 'languages=' + language_section + '&'
                        elif sort_by == 'user_rating':
                            language_url = self.get_url() + 'search/title?' + url_filter_language_rated_movie + url_type_movie + 'languages=' + language_section + '&'
                        else:
                            language_url = self.get_url() + 'search/title?' + url_filter_language_movie + url_type_movie + 'languages=' + language_section + '&'
                        self.AddSection(list, indexer, language_section, language_title, language_url + url_default_movie_language, indexer)
                    elif indexer == common.indxr_TV_Shows:
                        sort_by = self.Settings().get_setting('tvshow_GetSortByOptions_language')
                        if sort_by == 'user_rating':
                            language_url = self.get_url() + 'search/title?' + url_filter_language_rated_tvshow + url_type_tvshow + 'languages=' + language_section + '&'
                        else:
                            language_url = self.get_url() + 'search/title?' + url_filter_language_tvshow + url_type_tvshow + 'languages=' + language_section + '&'
                        self.AddSection(list, indexer, language_section, language_title, language_url + url_default_tvshow_language, indexer)

        elif section == 'people':#(no filter)*
            if indexer == common.indxr_Lists:
                self.AddSection(list, indexer, 'search_gender', 'Most Popular People', self.get_url()+'search/name?' + 'gender=female,male&' + '&sort=starmeter,asc', indexer)
                self.AddSection(list, indexer, 'search_gender', 'Most Popular People Born Today', self.get_url()+'search/name?' + 'birth_monthday=' + str(todays_date.month) + '-' + str(todays_date.day) + '&sort=starmeter,asc', indexer)
                self.AddSection(list, indexer, 'search_gender', 'Most Popular Deceased People', self.get_url()+'search/name?' + 'death_date=,' + str(todays_date.isoformat()) + '&sort=starmeter,asc', indexer)
                self.AddSection(list, indexer, 'search_gender', 'Oscar-Winning People' + userlist_People_GetSortByOptions, self.get_url()+'search/name?' + 'gender=female,male&' + 'groups=oscar_winners&' + url_default_userlist_people, indexer)
                self.AddSection(list, indexer, 'search_gender_director', 'Best Director-Winning People' + userlist_People_GetSortByOptions, self.get_url()+'search/name?' + 'groups=oscar_best_director_winners&' + url_default_userlist_people, indexer)
                self.AddSection(list, indexer, 'search_gender_director', 'Best Director-Nominated People' + userlist_People_GetSortByOptions, self.get_url()+'search/name?' + 'groups=oscar_best_director_nominees&' + url_default_userlist_people, indexer)
                self.AddSection(list, indexer, 'search_gender', 'Top 100 Stars of 2014' + userlist_People_GetSortByOptions, self.get_url()+'search/name?lists=' + 'ls071835930' + '&' + url_default_userlist_people, indexer)
                self.AddSection(list, indexer, 'search_gender_actor', 'Top 20 Actresses of the Last 20 Years' + userlist_People_GetSortByOptions, self.get_url()+'search/name?lists=' + 'ls000000708' + '&' + url_default_userlist_people, indexer)
                self.AddSection(list, indexer, 'search_gender_actor', 'Top 20 Actors of the Last 20 Years' + userlist_People_GetSortByOptions, self.get_url()+'search/name?lists=' + 'ls000000586' + '&' + url_default_userlist_people, indexer)
                self.AddSection(list, indexer, 'search_gender_writer', 'Top 20 Writers of the Past 20 Years' + userlist_People_GetSortByOptions, self.get_url()+'search/name?lists=' + 'ls000000486' + '&' + url_default_userlist_people, indexer)
                self.AddSection(list, indexer, 'search_gender_producer', 'Top Producers' + userlist_People_GetSortByOptions, self.get_url()+'search/name?lists=' + 'ls052049585' + '&' + url_default_userlist_people, indexer)
                self.AddSection(list, indexer, 'search_gender_actor', 'Female Action Stars' + userlist_People_GetSortByOptions, self.get_url()+'search/name?lists=' + 'ls059545963' + '&' + url_default_userlist_people, indexer)

        elif section == 'theaters':#(json, no filter)*
            if indexer == common.indxr_Movies:
                if self.Settings().get_setting('topboxoffice')=='true':
                    self.AddSection(list, indexer, 'json', 'US Box Office', self.get_m_url()+ 'boxoffice_json', indexer)
                if self.Settings().get_setting('theaters_soon')=='true':
                    self.AddSection(list, indexer, 'json', 'Theaters: Coming Soon', self.get_m_url()+ 'nowplaying_json', indexer)
        else:
            print 'presume ExtractContentAndAddtoList'
            print 'url ' + str(url)
            print 'type ' + type + '|page ' + page + '|total pages ' + total_pages + '|sort by ' + sort_by + '|sort order ' + sort_order

            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

    def get_sub_genres(self, indexer, section, genre_section, genre_url_no_type, genre_title, list):
        import datetime

        # Get a date object
        todays_date = datetime.date.today()
        now_playing_weeks_us = self.Settings().get_setting('now_playing_weeks_us')
        search_now_playing_date = todays_date + datetime.timedelta(weeks=-int(now_playing_weeks_us))

        url_type_movie = 'title_type=feature,tv_movie,video,tv_special,short&'
        url_type_tvshow = 'title_type=tv_series,mini_series&'

        if self.Settings().get_setting('ShowSortByOptions')=='true':
            dict = self.GetSortByOptions()
            movie_GetSortByOptions_now_playing_us = ' [' + dict[self.Settings().get_setting('movie_GetSortByOptions_now_playing_us')] + ']'
            movie_GetSortByOptions_awards = ' [' + dict[self.Settings().get_setting('movie_GetSortByOptions_awards')] + ']'
            movie_GetSortByOptions_awards_tv = ' [' + dict[self.Settings().get_setting('movie_GetSortByOptions_awards_tv')] + ']'
            movie_GetSortByOptions_imdb_ratings = ' [' + dict[self.Settings().get_setting('movie_GetSortByOptions_imdb_ratings')] + ']'

            tvshow_GetSortByOptions_awards = ' [' + dict[self.Settings().get_setting('tvshow_GetSortByOptions_awards')] + ']'

        else:
            movie_GetSortByOptions_now_playing_us = ''
            movie_GetSortByOptions_awards = ''
            movie_GetSortByOptions_awards_tv = ''
            movie_GetSortByOptions_imdb_ratings = ''

            tvshow_GetSortByOptions_awards = ''

        if self.Settings().get_setting('genres_submenu')=='true':
            if indexer == common.indxr_Movies:
                url_default_movie_awards = 'sort=' + self.Settings().get_setting('movie_GetSortByOptions_awards') + ',' + self.Settings().get_setting('movie_GetSortOrderOptions_awards')
                url_default_movie_awards_tv = 'sort=' + self.Settings().get_setting('movie_GetSortByOptions_awards_tv') + ',' + self.Settings().get_setting('movie_GetSortOrderOptions_awards_tv')
                url_default_movie_now_playing_us = 'sort=' + self.Settings().get_setting('movie_GetSortByOptions_now_playing_us') + ',' + self.Settings().get_setting('movie_GetSortOrderOptions_now_playing_us')
                url_default_movie_imdb_ratings = 'sort=' + self.Settings().get_setting('movie_GetSortByOptions_imdb_ratings') + ',' + self.Settings().get_setting('movie_GetSortOrderOptions_imdb_ratings')

                if genre_section == 'documentary':
                    if section in ['genres','genres_feature']:
                        self.AddSection(list, indexer, genre_section + '_now-playing-us', genre_title + ' Now Playing US' + movie_GetSortByOptions_now_playing_us, genre_url_no_type + '&' + 'title_type=documentary&' + 'groups=now-playing-us&' + 'release_date=' + str(search_now_playing_date) + ',&' + url_default_movie_now_playing_us, indexer, hlevel=2)#
                    self.AddSection(list, indexer, genre_section + '_oscar_nominees', genre_title + ' Oscar-Nominated' + movie_GetSortByOptions_awards, genre_url_no_type + '&' + 'title_type=documentary&' + 'groups=oscar_nominees&' + url_default_movie_awards_tv, indexer, hlevel=2)
                    self.AddSection(list, indexer, genre_section + '_emmy_nominees', genre_title + ' Emmy Award-Nominated' + movie_GetSortByOptions_awards_tv, genre_url_no_type + '&' + 'title_type=documentary&' + 'groups=emmy_nominees&' + url_default_movie_awards_tv, indexer, hlevel=2)
                else:
                    if section == 'genres':
                        self.AddSection(list, indexer, genre_section + '_now-playing-us', genre_title + ' Now Playing US' + movie_GetSortByOptions_now_playing_us, genre_url_no_type + '&' + url_type_movie + 'groups=now-playing-us&' + 'release_date=' + str(search_now_playing_date) + ',&' + url_default_movie_now_playing_us, indexer, hlevel=2)#
                        self.AddSection(list, indexer, genre_section + '_top_1000', genre_title + ' IMDb Top 1000' + movie_GetSortByOptions_imdb_ratings, genre_url_no_type + '&' + url_type_movie + 'groups==top_1000&' + url_default_movie_imdb_ratings, indexer, hlevel=2)#
                        self.AddSection(list, indexer, genre_section + '_oscar_nominees', genre_title + ' Oscar-Nominated' + movie_GetSortByOptions_awards, genre_url_no_type + '&' + url_type_movie + 'groups=oscar_nominees&' + url_default_movie_awards, indexer, hlevel=2)
                        self.AddSection(list, indexer, genre_section + '_emmy_nominees', genre_title + ' Emmy Award-Nominated' + movie_GetSortByOptions_awards_tv, genre_url_no_type + '&' + url_type_movie + 'groups=emmy_nominees&' + url_default_movie_awards_tv, indexer, hlevel=2)
                    elif section == 'genres_feature':
                        self.AddSection(list, indexer, genre_section + '_now-playing-us', genre_title + ' Now Playing US' + movie_GetSortByOptions_now_playing_us, genre_url_no_type + '&' + 'title_type=feature&' + 'groups=now-playing-us&' + 'release_date=' + str(search_now_playing_date) + ',&' + url_default_movie_now_playing_us, indexer, hlevel=2)#
                        self.AddSection(list, indexer, genre_section + '_top_1000', genre_title + ' IMDb Top 1000' + movie_GetSortByOptions_imdb_ratings, genre_url_no_type + '&' + 'title_type=feature&' + 'groups==top_1000&' + url_default_movie_imdb_ratings, indexer, hlevel=2)#
                        self.AddSection(list, indexer, genre_section + '_oscar_nominees', genre_title + ' Oscar-Nominated' + movie_GetSortByOptions_awards, genre_url_no_type + '&' + 'title_type=feature&' + 'groups=oscar_nominees&' + url_default_movie_awards, indexer, hlevel=2)
                    elif section == 'genres_tv_movie_tv_special':
                        self.AddSection(list, indexer, genre_section + '_emmy_nominees', genre_title + ' Emmy Award-Nominated' + movie_GetSortByOptions_awards_tv, genre_url_no_type + '&' + 'title_type=tv_movie,tv_special&' + 'groups=emmy_nominees&' + url_default_movie_awards_tv, indexer, hlevel=2)
                    elif section == 'genres_short':
                        self.AddSection(list, indexer, genre_section + '_oscar_nominees', genre_title + ' Oscar-Nominated' + movie_GetSortByOptions_awards_tv, genre_url_no_type + '&' + 'title_type=short&' + 'groups=oscar_nominees&' + url_default_movie_awards_tv, indexer, hlevel=2)

            elif indexer == common.indxr_TV_Shows:
                url_default_tvshow_awards = 'sort=' + self.Settings().get_setting('tvshow_GetSortByOptions_awards') + ',' + self.Settings().get_setting('tvshow_GetSortOrderOptions_awards')
                if section == 'genres':
                    self.AddSection(list, indexer, genre_section + '_emmy_nominees', genre_title + ' Emmy Award-Nominated' + tvshow_GetSortByOptions_awards, genre_url_no_type + '&' + url_type_tvshow + 'groups=emmy_nominees&' + url_default_tvshow_awards, indexer, hlevel=2)

    #request: it would be nice when you select user rating that the sort order would change to descending automatic.
    #sorting alphabet is not working 100%.

    def GetSortByOptions(self): 

        from entertainment import odict
        sort_by_dict = odict.odict()

        sort_by_dict['alpha'] = 'Alphabet (People, Watchlist)'
        sort_by_dict['user_rating'] = 'Ratings'
        sort_by_dict['boxoffice_gross_us'] = 'Box Office'
        sort_by_dict['moviemeter'] = 'Views'
        sort_by_dict['num_votes'] = 'Votes'
        sort_by_dict['year'] = 'Year'
        sort_by_dict['release_date_us'] = 'Release Date US'
        sort_by_dict['runtime'] = 'Runtime'
        sort_by_dict['ir'] = 'IMDb Rating (Charts)'
        sort_by_dict['nv'] = 'Number of Ratings (Charts)'
        sort_by_dict['rd'] = 'US Release Date (Charts)'
        sort_by_dict['starmeter'] = 'Views (People)'
        sort_by_dict['height'] = 'Height (People)'
        sort_by_dict['birth_date'] = 'Birth Date (People)'
        sort_by_dict['death_date'] = 'Death Date (People)'
        sort_by_dict['release_date'] = 'Release Date (People)'
        sort_by_dict['list_order'] = 'List Order (Watchlist)'
        sort_by_dict['date_added'] = 'Date Added (Watchlist)'

        return sort_by_dict

    def GetSortOrderOptions(self):
        
        from entertainment import odict
        sort_order_dict = odict.odict()
        
        sort_order_dict['asc'] = 'Ascending'
        sort_order_dict['desc'] = 'Descending'
        
        return sort_order_dict
        
    def Search(self, indexer, keywords, type, list, lock, message_queue, page='', total_pages=''): 

        from entertainment.net import Net
        net = Net() 
        
        keywords = self.CleanTextForSearch(keywords) 
        
        keywords_lower = keywords.lower().split(' ')
        match_total = float( len(keywords_lower) )
        
        from entertainment import odict
        search_dict = odict.odict({ 's' : 'tt', 'q' : keywords})
        
        if indexer == common.indxr_Movies:
            search_dict.update({'ttype':'ft'})
        elif indexer == common.indxr_TV_Shows:
            search_dict.update({'ttype':'tv'})
        
        search_dict.sort(key=lambda x: x[0].lower())
                
        import urllib
        search_for_url = self.get_url() + 'find?' + urllib.urlencode(search_dict)

        if self.Settings().get_setting('en_us')=='true':
            content = net.http_GET(search_for_url,{'Accept-Language':'en-US'}).content
        else:
            content = net.http_GET(search_for_url).content
        if '<h1 class="findHeader">No results found' in content:
            return
            
        self.AddInfo(list, indexer, 'search', self.get_url(), type, '1', '1')
      
        
        mode = common.mode_File_Hosts
        if type == 'tv_shows':
            mode = common.mode_Content
            type = 'tv_seasons'
        
        import re
        
        search_results = re.search('(?s)<table class="findList">(.+?)</table>', content)
        
        if search_results:            
            search_results = search_results.group(1)
            
            search_term_not_found_count = 0
            for search_item in re.finditer('<td class="result_text"> <a href="/title/(.+?)/.+?" >(.+?)</a> (.+?) <(.+?)</td>', content):
            
                item_id = search_item.group(1)
                item_url = self.get_url() + 'title/' + item_id
                
                item_name = search_item.group(2)
                item_name_lower = item_name.lower()
                
                match_count = 0
                for kw in keywords_lower:
                    if kw in item_name_lower:
                        match_count = match_count + 1

                match_fraction = ( match_count / match_total )

                if not ( match_fraction >= 0.8  ):

                    aka_item = search_item.group(4)

                    aka_name = re.search('aka <i>"(.+?)"</i>', aka_item)
                    if aka_name:
                        item_name = aka_name.group(1)
                        item_name_lower = item_name.lower()
                        match_count = 0
                        for kw in keywords_lower:
                            if kw in item_name_lower:
                                match_count = match_count + 1
                        match_fraction = ( match_count / match_total )
                        if not ( match_fraction >= 0.8  ):
                            search_term_not_found_count += 1
                            if search_term_not_found_count >= 2:
                                break
                            else:
                                continue
                    else:
                        search_term_not_found_count += 1
                        if search_term_not_found_count >= 2:
                            break
                        else:
                            continue
                
                item_title = item_name
                item_other_info = search_item.group(3)
                item_year = re.search('\(([0-9]+)\)', item_other_info)
                if item_year:
                    item_year = item_year.group(1)
                    item_title += ' (' + item_year + ')'
                else:
                    item_year = ''
        
        
                if 'movie' in item_other_info.lower():
                    type = common.indxr_Movies 
                    mode = common.mode_File_Hosts
                    indexer = common.indxr_Movies                     
                elif 'series' in item_other_info.lower():
                    type = 'tv_seasons'
                    mode = common.mode_Content
                    indexer = common.indxr_TV_Shows 
                    
                self.AddContent(list, indexer, mode, item_title, '', type, url=item_url, name=item_name, year=item_year, imdb_id=item_id)
