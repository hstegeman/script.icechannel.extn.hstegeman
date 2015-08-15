'''
    Freeomovie
    14-6-15
'''
from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

class freeomovie(MovieIndexer, MovieSource, CustomSettings):
    implements = [MovieIndexer, MovieSource, CustomSettings]
    
    name = "Freeomovie"
    display_name = "Freeomovie"

    base_url = 'http://www.freeomovie.com'

    default_indexer_enabled = 'false'
    source_enabled_by_default = 'false'

    '''
    http://www.freeomovie.com/robots.txt
    http://www.freeomovie.com/sitemap.xml
    '''

    def __init__(self):

        pages_count_list = '-|1|2|3|4|5|10|15|20|25|30|40|50|75|100|150|200|250|500'

        xml = '<settings>\n'
        xml += '<category label="Freeomovie SETTINGS">\n'
        xml += '<setting id="maximum_pages_count" label="Maximum pages count" type="labelenum" default="-" values=' + pages_count_list + ' />\n'

        xml += '</category>\n'
        xml += '</settings>\n'

        self.CreateSettings(self.name, self.display_name, xml)

    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):

        new_url = url

        maximum_pages_count = self.Settings().get_setting('maximum_pages_count')

        if page == '':
            page = '1'
        else:
            page = str(int(page))

        if section == 'xsearch':
            new_url = new_url.replace('/?s=', '/page/' + str(page) + '/?s=')

        else:
            new_url = new_url + 'page/' + str(page) + '/'

        print 'new_url ' + new_url

        from entertainment.net import Net
        import re
        net = Net(cached=True)
        import urllib

        content = net.http_GET(new_url).content
        item_re = '<div class="boxentry">\s*<a href="(.+?)" title="(.+?)">\s*<img src="(.+?)"'


        if total_pages == '':
            np=re.compile('<a class="last" href=".+?/page/([0-9,]+)/">Last').findall(content)

            if len(np) == 0:
                np=re.compile('<a class="page larger" href=".+?">([0-9,]+)</a>',re.MULTILINE|re.DOTALL).findall(content)

            if len(np) > 0:
                lp = len(np)-1
                total_pages = np[lp]
                print 'total_pages ' + str(total_pages)

            else:
                total_pages = '1'

            if section in ['recent_videos','full_movies']:
                if maximum_pages_count != '-':
                    if int(total_pages) > int(maximum_pages_count):
                        total_pages = maximum_pages_count

            print 'total_pages ' + str(total_pages)

        self.AddInfo(list, indexer, section, url, type, page, total_pages)

        match=re.compile(item_re).findall(content)

        for url,name,thumbnail in match:
            try:
                name = self.CleanTextForSearch(name)
                name = name.encode('ascii', 'ignore')

                print 'presume addcontent'
                print 'indexer ' + str(indexer) + '|item type ' + str(type) + '|name ' + name + '|thumbnail ' + str(thumbnail)
                print 'url ' + str(url)

                self.AddContent(list, indexer, common.mode_File_Hosts, name, '', type, url=url, name=name, img=thumbnail)
            except:
                print 'not ' + str(name)

                continue

    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):

        if indexer == common.indxr_Movies:

            if section == 'main':
                #self.AddSection(list, indexer, 'recent_videos', 'New Movies', self.base_url + '/2015/', indexer)
                #self.AddSection(list, indexer, 'recent_videos', 'Recent Videos', self.base_url + '/', indexer)
                self.AddSection(list, indexer, 'full_movies', 'XXX Movies', self.base_url + '/category/full-movie/', indexer)
                self.AddSection(list, indexer, 'clips', 'XXX Scenes', self.base_url + '/category/clips/', indexer)
                self.AddSection(list, indexer, 'categories', 'Categories')
                self.AddSection(list, indexer, 'tags', 'Tags')
                self.AddSection(list, indexer, 'distributors', 'Distributors')
                self.AddSection(list, indexer, 'movie_sets', 'Movie Sets')
                self.AddSection(list, indexer, 'archive', 'Archive')
                self.AddSection(list, indexer, 'people', 'Peoples')

            elif section == 'categories':

                import re

                from entertainment.net import Net
                net = Net()

                category_re = ''

                category_url = self.base_url + '/'

                if indexer == common.indxr_Movies:
                    category_re = '(?s)<div class="multi-column-taxonomy-list">(.+?)</div>'

                content = net.http_GET(category_url).content

                categories = re.search(category_re, content)
                if categories:
                    categories = categories.group(1)

                    for category in re.finditer('<a href="(.+?)" rel="tag">(.+?)</a>', categories):
                        category_url = category.group(1)
                        category_title = category.group(2)

                        self.AddSection(list, indexer, 'category_section', category_title, category_url, indexer)

            elif section == 'tags':
                self.AddSection(list, indexer, 'xsearch', 'Anal XXX Scenes', self.base_url + '/category/clips/?s=anal', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Anal Extreme', self.base_url + '/category/anal/?s=extreme', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Anal Fisting', self.base_url + '/category/anal/?s=fisting', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Anal Gaping', self.base_url + '/category/anal/?s=gaping', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Bizarre', self.base_url + '/?s=bizarre', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Celebrity', self.base_url + '/?s=celebrity', indexer)


                self.AddSection(list, indexer, 'xsearch', 'Double Anal', self.base_url + '/?s=%22double+anal%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Fisting', self.base_url + '/?s=fisting', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Orgy', self.base_url + '/?s=orgy', indexer)
                self.AddSection(list, indexer, 'tags_section', 'Reality', self.base_url + '/tag/reality/', indexer)
                self.AddSection(list, indexer, 'tags_section', 'Squirting', self.base_url + '/tag/squirting/', indexer)
                self.AddSection(list, indexer, 'tags_section', 'Uncensored', self.base_url + '/tag/uncensored/', indexer)

            elif section == 'archive':
                self.AddSection(list, indexer, 'archive_year', 'Archive By Year')
                self.AddSection(list, indexer, 'archive_month', 'Archive By Month')

            elif section == 'archive_year':
                self.AddSection(list, indexer, 'archive_2015', '2015', self.base_url + '/2015/', indexer)
                self.AddSection(list, indexer, 'archive_2014', '2014', self.base_url + '/2014/', indexer)
                self.AddSection(list, indexer, 'archive_2013', '2013', self.base_url + '/2013/', indexer)

            elif section == 'archive_month':
                self.AddSection(list, indexer, 'archive_section', '2015/06', self.base_url + '/2015/06/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2015/05', self.base_url + '/2015/05/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2015/04', self.base_url + '/2015/04/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2015/03', self.base_url + '/2015/03/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2015/02', self.base_url + '/2015/02/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2015/01', self.base_url + '/2015/01/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2014/12', self.base_url + '/2014/12/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2014/11', self.base_url + '/2014/11/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2014/10', self.base_url + '/2014/10/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2014/09', self.base_url + '/2014/09/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2014/08', self.base_url + '/2014/08/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2014/07', self.base_url + '/2014/07/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2014/06', self.base_url + '/2014/06/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2014/05', self.base_url + '/2014/05/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2014/04', self.base_url + '/2014/04/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2014/03', self.base_url + '/2014/03/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2014/02', self.base_url + '/2014/02/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2014/01', self.base_url + '/2014/01/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2013/12', self.base_url + '/2013/12/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2013/11', self.base_url + '/2013/11/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2013/10', self.base_url + '/2013/10/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2013/09', self.base_url + '/2013/09/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2013/08', self.base_url + '/2013/08/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2013/07', self.base_url + '/2013/07/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2013/06', self.base_url + '/2013/06/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2013/05', self.base_url + '/2013/05/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2013/04', self.base_url + '/2013/04/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2013/03', self.base_url + '/2013/03/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2013/02', self.base_url + '/2013/02/', indexer)
                self.AddSection(list, indexer, 'archive_section', '2013/01', self.base_url + '/2013/01/', indexer)

            elif section == 'people':
                self.AddSection(list, indexer, 'actrices', 'Actrices')
                self.AddSection(list, indexer, 'actors', 'Actors')

            elif section == 'actrices':
                self.AddSection(list, indexer, 'actrice', 'Abbie Cat', self.base_url + '/tag/abbie-cat/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Adriana Chechik', self.base_url + '/tag/adriana-chechik/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Adrianna Luna', self.base_url + '/tag/adrianna-luna/', indexer)
                self.AddSection(list, indexer, 'actrice', 'AJ Applegate', self.base_url + '/tag/aj-applegate/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Alektra Blue', self.base_url + '/tag/alektra-blue/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Alexis Ford', self.base_url + '/tag/alexis-ford/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Alexis Texas', self.base_url + '/tag/alexis-texas/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Alina Li', self.base_url + '/tag/alina-li/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Aline', self.base_url + '/tag/aline/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Allie Haze', self.base_url + '/tag/allie-haze/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Alysa', self.base_url + '/tag/alysa/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Amber Rayne', self.base_url + '/tag/amber-rayne/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Amy Brooke', self.base_url + '/tag/amy-brooke/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Andy San Dimas', self.base_url + '/tag/andy-san-dimas/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Angel Dark', self.base_url + '/tag/angel-dark/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Angel Rivas', self.base_url + '/tag/angel-rivas/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Angelina Crow', self.base_url + '/tag/angelina-crow/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Anikka Albrite', self.base_url + '/tag/anikka-albrite/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Anissa Kate', self.base_url + '/tag/anissa-kate/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Annie Cruz', self.base_url + '/tag/annie-cruz/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Ariel-X', self.base_url + '/tag/ariel-x/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Asa Akira', self.base_url + '/tag/asa-akira/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Ash Hollywood', self.base_url + '/tag/ash-hollywood/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Ashley Blue', self.base_url + '/tag/ashley-blue/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Ashley Fires', self.base_url + '/tag/ashley-fires/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Ashli Orion', self.base_url + '/tag/ashli-orion/', indexer)
                self.AddSection(list, indexer, 'actrice', 'August Ames', self.base_url + '/tag/august-ames/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Aurora Snow', self.base_url + '/tag/aurora-snow/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Ava Addams', self.base_url + '/tag/ava-addams/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Ava Devine', self.base_url + '/tag/ava-devine/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Belladonna', self.base_url + '/tag/belladonna/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Black Angelika', self.base_url + '/tag/black-angelika/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Bobbi Eden', self.base_url + '/tag/bobbi-eden/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Bobbi Starr', self.base_url + '/tag/bobbi-starr/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Bonnie Rotten', self.base_url + '/tag/bonnie-rotten/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Bonny Bon', self.base_url + '/tag/bonny-bon/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Bree Olson', self.base_url + '/tag/bree-olson/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Brianna Love', self.base_url + '/tag/brianna-love/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Britney', self.base_url + '/tag/britney/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Carla Cox', self.base_url + '/tag/carla-cox/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Carmella Bing', self.base_url + '/tag/carmella-bing/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Carter Cruise', self.base_url + '/tag/carter-cruise/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Casey Calvert', self.base_url + '/tag/casey-calvert/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Cassandra Nix', self.base_url + '/tag/cassandra-nix/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Chanel Preston', self.base_url + '/tag/chanel-preston/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Charley Chase', self.base_url + '/tag/charley-chase/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Chastity Lynn', self.base_url + '/tag/chastity-lynn/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Chelsie Rae', self.base_url + '/tag/chelsie-rae/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Cherie Deville', self.base_url + '/tag/cherie-deville/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Cherry Jul', self.base_url + '/tag/cherry-jul/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Cindy Starfall', self.base_url + '/tag/cindy-starfall/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Clara G', self.base_url + '/tag/clara-g/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Dahlia Sky', self.base_url + '/tag/dahlia-sky/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Dakota Skye', self.base_url + '/tag/dakota-skye/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Dana Dearmond', self.base_url + '/tag/dana-dearmond/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Dana Vespoli', self.base_url + '/tag/dana-vespoli/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Devon', self.base_url + '/tag/devon/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Dillion Harper', self.base_url + '/tag/dillion-harper/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Dora Venter', self.base_url + '/tag/dora-venter/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Ellen Saint', self.base_url + '/tag/ellen-saint/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Eufrat', self.base_url + '/tag/eufrat/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Eva Karera', self.base_url + '/tag/eva-karera/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Felecia', self.base_url + '/tag/felecia/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Francesca Le', self.base_url + '/tag/francesca-le/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Franceska Jaimes', self.base_url + '/tag/franceska-jaimes/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Gabriella Paltrova', self.base_url + '/tag/gabriella-paltrova/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Gauge', self.base_url + '/tag/gauge/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Holly Hanna', self.base_url + '/tag/holly-hanna/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Holly Heart', self.base_url + '/tag/holly-heart/', indexer)
                self.AddSection(list, indexer, 'actrice', 'India Summer', self.base_url + '/tag/india-summer/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Isabella Clark', self.base_url + '/tag/isabella-clark/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Isis Love', self.base_url + '/tag/isis-love/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Jada Fire', self.base_url + '/tag/jada-fire/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Jada Stevens', self.base_url + '/tag/jada-stevens/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Jayden Jaymes', self.base_url + '/tag/jayden-jaymes/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Jayden Lee', self.base_url + '/tag/jayden-lee/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Jesse Jane', self.base_url + '/tag/jesse-jane/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Jessica Bangkok', self.base_url + '/tag/jessica-bangkok/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Jessie Andrews', self.base_url + '/tag/jessie-andrews/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Julia Ann', self.base_url + '/tag/julia-ann/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Kagney Linn Karter', self.base_url + '/tag/kagney-linn-karter/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Katsuni', self.base_url + '/tag/katsuni/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Kayden Kross', self.base_url + '/tag/kayden-kross/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Keisha Grey', self.base_url + '/tag/keisha-grey/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Kristina Rose', self.base_url + '/tag/kristina-rose/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Laela Pryce', self.base_url + '/tag/laela-pryce/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Lea Lexis', self.base_url + '/tag/lea-lexis/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Lexi Belle', self.base_url + '/tag/lexi-belle/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Lexi Love', self.base_url + '/tag/lexi-love/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Lily Labeau', self.base_url + '/tag/lily-labeau/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Lisa Ann', self.base_url + '/tag/lisa-ann/', indexer)
                self.AddSection(list, indexer, 'actrice', 'London Keyes', self.base_url + '/tag/london-keyes/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Lou Charmelle', self.base_url + '/tag/lou-charmelle/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Maddy Oreilly', self.base_url + '/tag/maddy-oreilly/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Mandy Bright', self.base_url + '/tag/mandy-bright/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Marica Hase', self.base_url + '/tag/marica-hase/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Marina Visconti', self.base_url + '/tag/marina-visconti/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Maya Hills', self.base_url + '/tag/maya-hills/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Mia Malkova', self.base_url + '/tag/mia-malkova/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Misha Cross', self.base_url + '/tag/misha-cross/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Naomi', self.base_url + '/tag/naomi/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Naughty Alysha', self.base_url + '/tag/naughty-alysha/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Nikita Bellucci', self.base_url + '/tag/nikita-bellucci/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Nikki Sexx', self.base_url + '/tag/nikki-sexx/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Nikky Thorn', self.base_url + '/tag/nikky-thorn/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Penny Pax', self.base_url + '/tag/penny-pax/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Phoenix Marie', self.base_url + '/tag/phoenix-marie/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Proxy Paige', self.base_url + '/tag/proxy-paige/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Rebeca Linares', self.base_url + '/tag/rebeca-linares/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Remy LaCroix', self.base_url + '/tag/remy-lacroix/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Renee Pornero', self.base_url + '/tag/renee-pornero/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Riley Reid', self.base_url + '/tag/riley-reid/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Riley Steele', self.base_url + '/tag/riley-steele/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Rita Faltoyano', self.base_url + '/tag/rita-faltoyano/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Roxy Raye', self.base_url + '/tag/roxy-raye/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Samantha Saint', self.base_url + '/tag/samantha-saint/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Sandra Romain', self.base_url + '/tag/sandra-romain/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Sarah Shevon', self.base_url + '/tag/sarah-shevon/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Sarah Vandella', self.base_url + '/tag/sarah-vandella/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Sasha Grey', self.base_url + '/tag/sasha-grey/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Savannah Fox', self.base_url + '/tag/savannah-fox/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Selena Rose', self.base_url + '/tag/selena-rose/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Shannya Tweeks', self.base_url + '/tag/shannya-tweeks/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Sharka Blue', self.base_url + '/tag/sharka-blue/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Sheena Ryder', self.base_url + '/tag/sheena-ryder/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Sheena Shaw', self.base_url + '/tag/sheena-shaw/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Sierra Sanders', self.base_url + '/tag/sierra-sanders/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Sindee Jennings', self.base_url + '/tag/sindee-jennings/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Sinn Sage', self.base_url + '/tag/sinn-sage/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Siri', self.base_url + '/tag/siri/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Skin Diamond', self.base_url + '/tag/skin-diamond/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Sophie Dee', self.base_url + '/tag/sophie-dee/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Stormy Daniels', self.base_url + '/tag/stormy-daniels/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Stoya', self.base_url + '/tag/stoya/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Summer Brielle', self.base_url + '/tag/summer-brielle/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Suzie Diamond', self.base_url + '/tag/suzie-diamond/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Syren De Mer', self.base_url + '/tag/syren-de-mer/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Tarra White', self.base_url + '/tag/tarra-white/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Tori Black', self.base_url + '/tag/tori-black/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Tory Lane', self.base_url + '/tag/tory-lane/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Trina Michaels', self.base_url + '/tag/trina-michaels/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Valentina Nappi', self.base_url + '/tag/valentina-nappi/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Veronica Avluv', self.base_url + '/tag/veronica-avluv/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Veruca James', self.base_url + '/tag/veruca-james/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Vicki Chase', self.base_url + '/tag/vicki-chase/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Wiska', self.base_url + '/tag/wiska/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Zafira', self.base_url + '/tag/zafira/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Zoey Monroe', self.base_url + '/tag/zoey-monroe/', indexer)
                self.AddSection(list, indexer, 'actrice', 'Zoey Portland', self.base_url + '/tag/zoey-portland/', indexer)

                '''
                self.AddSection(list, indexer, 'actrice', 'XXX', self.base_url + '/tag/XXX/', indexer)
                self.AddSection(list, indexer, 'actrice', 'XXX', self.base_url + '/tag/XXX/', indexer)
                self.AddSection(list, indexer, 'actrice', 'XXX', self.base_url + '/tag/XXX/', indexer)

                '''

            elif section == 'actors':
                self.AddSection(list, indexer, 'actor', 'Anthony Rosano', self.base_url + '/tag/anthony-rosano/', indexer)
                self.AddSection(list, indexer, 'actor', 'Danny Mountain', self.base_url + '/tag/danny-mountain/', indexer)
                self.AddSection(list, indexer, 'actor', 'David Perry', self.base_url + '/tag/david-perry/', indexer)
                self.AddSection(list, indexer, 'actor', 'Erik Everhard', self.base_url + '/tag/erik-everhard/', indexer)
                self.AddSection(list, indexer, 'actor', 'Evan Stone', self.base_url + '/tag/evan-stone/', indexer)
                self.AddSection(list, indexer, 'actor', 'Ian Scott', self.base_url + '/tag/ian-scott/', indexer)
                self.AddSection(list, indexer, 'actor', 'James Deen', self.base_url + '/tag/james-deen/', indexer)
                self.AddSection(list, indexer, 'actor', 'John Strong', self.base_url + '/tag/john-strong/', indexer)
                self.AddSection(list, indexer, 'actor', 'Mandingo', self.base_url + '/tag/mandingo/', indexer)
                self.AddSection(list, indexer, 'actor', 'Manuel Ferrara', self.base_url + '/tag/manuel-ferrara/', indexer)
                self.AddSection(list, indexer, 'actor', 'Mark Wood', self.base_url + '/tag/mark-wood/', indexer)
                self.AddSection(list, indexer, 'actor', 'Mick Blue', self.base_url + '/tag/mick-blue/', indexer)
                self.AddSection(list, indexer, 'actor', 'Mr Pete', self.base_url + '/tag/mr-pete/', indexer)
                self.AddSection(list, indexer, 'actor', 'Omar Galanti', self.base_url + '/tag/omar-galanti/', indexer)
                self.AddSection(list, indexer, 'actor', 'Rocco Siffredi', self.base_url + '/tag/rocco-siffredi/', indexer)
                self.AddSection(list, indexer, 'actor', 'Shane Diesel', self.base_url + '/tag/shane-diesel/', indexer)
                self.AddSection(list, indexer, 'actor', 'Shorty Mac', self.base_url + '/tag/shorty-mac/', indexer)
                self.AddSection(list, indexer, 'actor', 'Sledge Hammer', self.base_url + '/tag/sledge-hammer/', indexer)
                self.AddSection(list, indexer, 'actor', 'Steve Holmes', self.base_url + '/tag/steve-holmes/', indexer)
                self.AddSection(list, indexer, 'actor', 'Steven st Croix', self.base_url + '/tag/steven-st-croix/', indexer)
                self.AddSection(list, indexer, 'actor', 'Tommy Gunn', self.base_url + '/tag/tommy-gunn/', indexer)
                self.AddSection(list, indexer, 'actor', 'Tommy Pistol', self.base_url + '/tag/tommy-pistol/', indexer)
                self.AddSection(list, indexer, 'actor', 'Toni Ribas', self.base_url + '/tag/toni-ribas/', indexer)
                self.AddSection(list, indexer, 'actor', 'TT boy', self.base_url + '/tag/tt-boy/', indexer)
                self.AddSection(list, indexer, 'actor', 'Voodoo', self.base_url + '/tag/voodoo/', indexer)
                self.AddSection(list, indexer, 'actor', 'Wesley Pipes', self.base_url + '/tag/wesley-pipes/', indexer)
                self.AddSection(list, indexer, 'actor', 'Will Powers' , self.base_url + '/tag/will-powers/', indexer)
                self.AddSection(list, indexer, 'actor', 'Xander Corvus', self.base_url + '/tag/xander-corvus/', indexer)

            elif section == 'distributors':
                self.AddSection(list, indexer, 'xsearch', '21sextury', self.base_url + '/?s=sextury', indexer)
                self.AddSection(list, indexer, 'distributor', 'Adam Eve', self.base_url + '/tag/adam-eve/', indexer)
                self.AddSection(list, indexer, 'distributor', 'American XXX Scenes', self.base_url + '/tag/american/', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Anarchy Films', self.base_url + '/?s=%22anarchy+films%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Atv', self.base_url + '/?s=atv', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Axel Braun', self.base_url + '/?s=%22axel+braun%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Brasileirinhas', self.base_url + '/?s=brasileirinhas', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Brazzers', self.base_url + '/?s=brazzers', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Christoph Clark', self.base_url + '/?s=%22christoph+clark%22', indexer)
                self.AddSection(list, indexer, 'distributor', 'Devils Films', self.base_url + '/tag/devils-films/', indexer)
                self.AddSection(list, indexer, 'distributor', 'Digital Sin', self.base_url + '/tag/digital-sin/', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Digital Playground', self.base_url + '/?s=%22digital+playground%22', indexer)

                self.AddSection(list, indexer, 'xsearch', 'Elegant Angel', self.base_url + '/?s=%22elegant+angel%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Erotica X', self.base_url + '/?s=%22erotica+x%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Evasive Angles', self.base_url + '/?s=%22evasive+angles%22', indexer)
                self.AddSection(list, indexer, 'distributor', 'Evil Angel', self.base_url + '/tag/evil-angel/', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Gangland', self.base_url + '/?s=gangland', indexer)
                self.AddSection(list, indexer, 'xsearch', 'GGG', self.base_url + '/?s=ggg', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Grazer', self.base_url + '/?s=grazer', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Hardx XXX Scenes', self.base_url + '/?s=hardx', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Harmony', self.base_url + '/?s=harmony', indexer)

                self.AddSection(list, indexer, 'xsearch', 'Hustler', self.base_url + '/?s=hustler', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Jay Sin', self.base_url + '/?s=%22jay+sin%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Jules Jordan', self.base_url + '/?s=%22jules+jordan%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Manuel Ferrara', self.base_url + '/?s=%22manuel+ferrara%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Naughty America', self.base_url + '/?s=%22naughty+america%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'New Sensations', self.base_url + '/?s=%22new+sensations%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Penthouse', self.base_url + '/?s=penthouse', indexer)

                self.AddSection(list, indexer, 'distributor', 'Private', self.base_url + '/tag/private/', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Pure Passion', self.base_url + '/?s=%22pure+passion%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Raul Christian', self.base_url + '/?s=%22raul+christian%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Raul Cristian', self.base_url + '/?s=%22raul+cristian%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Reality Junkies', self.base_url + '/?s=%22reality+junkies%22', indexer)
                #self.AddSection(list, indexer, 'xsearch', 'Reality Kings', self.base_url + '/?s=%22reality+kings%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Red Light District', self.base_url + '/?s=%22red+light+district%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Robby D', self.base_url + '/?s=%22robby+d%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Rocco', self.base_url + '/?s=rocco', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Russian Institute', self.base_url + '/?s=%22russian+institute%22', indexer)
                #self.AddSection(list, indexer, 'distributor', 'Simon Wolf', self.base_url + '/tag/simon-wolf/', indexer)
                self.AddSection(list, indexer, 'distributor', 'Smash Pictures', self.base_url + '/tag/smash-pictures/', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Sticky Video', self.base_url + '/?s=%22sticky+video%22', indexer)
                self.AddSection(list, indexer, 'distributor', 'Swank', self.base_url + '/tag/swank/', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Sweet Sinner', self.base_url + '/?s=%22sweet+sinner%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Teendorado', self.base_url + '/?s=teendorado', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Third Degree-films', self.base_url + '/?s=%22third+degree+films%22', indexer)
                #self.AddSection(list, indexer, 'xsearch', 'Tom Byron', self.base_url + '/?s=%22tom+byron%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Vca', self.base_url + '/?s=vca', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Videorama German', self.base_url + '/?s=videorama', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Viv Thomas', self.base_url + '/?s=%22viv+thomas%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Vivid', self.base_url + '/?s=vivid', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Vouyer Media', self.base_url + '/?s=%22vouyer+media%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'West Coast', self.base_url + '/?s=%22west+coast%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Wicked Pictures', self.base_url + '/?s=%22wicked+pictures%22', indexer)
                #self.AddSection(list, indexer, 'distributor', 'X-art', self.base_url + '/tag/x-art/', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Zero Tolerance', self.base_url + '/?s=%22zero+tolerance%22', indexer)

                '''
                self.AddSection(list, indexer, 'xsearch', 'xxx', self.base_url + '/?s=%22xxx%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'xxx', self.base_url + '/?s=%22xxx%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'xxx', self.base_url + '/?s=%22xxx%22', indexer)
                '''

            elif section == 'movie_sets':
                self.AddSection(list, indexer, 'xsearch', 'All Internal', self.base_url + '/?s=%22all+internal%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Anal Acrobats', self.base_url + '/?s=%22anal+acrobats%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Anal Agenda', self.base_url + '/?s=%22anal+agenda%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Anal Buffet', self.base_url + '/?s=%22anal+buffet%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Anal Cuties', self.base_url + '/?s=%22anal+cuties%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Anal Expedition', self.base_url + '/?s=%22anal+expedition%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Anal Students', self.base_url + '/?s=%22anal+students%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Anal Workout', self.base_url + '/?s=%22anal+workout%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Anally Yours', self.base_url + '/?s=%22anally+yours%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Angel Perverse', self.base_url + '/?s=%22angel+perverse%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Animal Trainer', self.base_url + '/?s=%22animal+trainer%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Asa Akira Is Insatiable', self.base_url + '/?s=%22asa+akira+is+insatiable%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Asian Booty', self.base_url + '/?s=%22asian+booty%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Asian Fucking Nation', self.base_url + '/?s=%22asian+fucking+nation%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'The Ass Party', self.base_url + '/?s=%22the+ass+party%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Ass Titans', self.base_url + '/?s=%22ass+titans%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Battle Of The Asses', self.base_url + '/?s=%22battle+of+the+asses%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Big Butts Like It Big', self.base_url + '/?s=%22big+butts+like+it+big%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Big Toy', self.base_url + '/?s=%22big+toy%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Big Wet Asses', self.base_url + '/?s=%22big+wet+asses%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Big Wet Brazilian Asses', self.base_url + '/?s=%22big+wet+brazilian+asses%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Black Listed', self.base_url + '/?s=%22black+listed%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Brazilian Babes', self.base_url + '/?s=%22brazilian+babes%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'The Brother Load', self.base_url + '/?s=%22the+brother+load%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Buttman Focused', self.base_url + '/?s=%22buttman+focused%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Church Of Bootyism', self.base_url + '/?s=%22church+of+bootyism%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Clusterfuck', self.base_url + '/?s=clusterfuck', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Cream Dreams', self.base_url + '/?s=%22cream+dreams%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Curvy Girls', self.base_url + '/?s=%22curvy+girls%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Dark Meat', self.base_url + '/?s=%22dark+meat%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Deep Anal Drilling', self.base_url + '/?s=%22deep+anal+drilling%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Dementia', self.base_url + '/?s=dementia', indexer)
                self.AddSection(list, indexer, 'xsearch', 'DP Fanatic', self.base_url + '/?s=%22dp+fanatic%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'DP My Wife With Me', self.base_url + '/?s=%22dp+my+wife+with+me%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Dressed To Fuck', self.base_url + '/?s=%22dressed+to+fuck%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Drunk Sex Orgy', self.base_url + '/?s=%22drunk+sex+orgy%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Elastic Assholes', self.base_url + '/?s=%22elastic+assholes%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Euro Angels', self.base_url + '/?s=%22euro+angels%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Euro Domination', self.base_url + '/?s=%22euro+domination%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Evil Anal', self.base_url + '/?s=%22evil+anal%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Extreme Penetrations', self.base_url + '/?s=%22extreme+penetrations%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Fetish Fanatic', self.base_url + '/?s=%22fetish+fanatic%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Fist Flush', self.base_url + '/?s=%22fist+flush%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Fresh On Cock', self.base_url + '/?s=%22fresh+on+cock%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Fuck Me Like A Whore', self.base_url + '/?s=%22fuck+me+like+a+whore%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Fuck My Ass', self.base_url + '/?s=%22fuck+my+ass%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Gang Bang Clips', self.base_url + '/category/clips/?s=gang+bang', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Gang Banged', self.base_url + '/?s=gangbanged', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Gangbang Auditions', self.base_url + '/?s=%22gangbang+auditions%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Gangbang Girl', self.base_url + '/?s=%22gangbang+girl%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Gangland Cream Pie', self.base_url + '/?s=%22gangland+cream+pie%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Girlvert', self.base_url + '/?s=girlvert', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Hard Bodies', self.base_url + '/?s=%22hard+bodies%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Hard Double Anal', self.base_url + '/?s=%22hard+double+anal%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Hose Monster', self.base_url + '/?s=%22hose+monster%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'I Love Big Toys', self.base_url + '/?s=%22i+love+big+toys%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'In Anal Sluts We Trust', self.base_url + '/?s=%22in+anal+sluts+we+trust%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Internal Damnation', self.base_url + '/?s=%22internal+damnation%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'The Le Wood Anal Hazing Crew', self.base_url + '/?s=%22the+le+wood+anal+hazing+crew%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Lesbain Anal POV', self.base_url + '/?s=%22lesbian+anal+pov%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Lex The Impaler', self.base_url + '/?s=%22lex+the+impaler%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Lex Turns Evil', self.base_url + '/?s=%22lex+turns+evil%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Lust Unleashed', self.base_url + '/?s=%22lust+unleashed%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Manhandled', self.base_url + '/?s=%22manhandled%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Massacre', self.base_url + '/?s=massacre', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Max Hardcore', self.base_url + '/?s=%22max+hardcore%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Maximum Perversion', self.base_url + '/?s=%22maximum+perversion%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Maximum Perversum', self.base_url + '/?s=%22maximum+perversum%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Milf Gape', self.base_url + '/?s=%22milf+gape%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'More Poles Than Holes', self.base_url + '/?s=%22more+poles+than+holes%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'My Huge Holes', self.base_url + '/?s=%22my+huge+holes%22', indexer)
                self.AddSection(list, indexer, 'xsearch', '... No Limits', self.base_url + '/?s=%22no+limits%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Oil Overload', self.base_url + '/?s=%22oil+overload%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Orgy Masters', self.base_url + '/?s=%22orgy+masters%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Perverse Babes', self.base_url + '/?s=%22perverse+babes%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Private Best Of', self.base_url + '/?s=%22private+best+of%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Private The Best By', self.base_url + '/?s=%22the+best+by+private%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Private Black Label', self.base_url + '/?s=%22private+black+label%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Private Gold', self.base_url + '/?s=%22private+gold%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Private Life', self.base_url + '/?s=%22private+life%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Private Movies', self.base_url + '/?s=%22private+movies%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Private Specials', self.base_url + '/?s=%22private+specials%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'The Private Story Of', self.base_url + '/?s=%22the+private+story+of%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Private Tropical', self.base_url + '/?s=%22private+tropical%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Private Xtreme', self.base_url + '/?s=%22private+xtreme%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Private XXX', self.base_url + '/?s=%22private+xxx%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Puppet Master', self.base_url + '/?s=%22puppet+master%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Real Adventures', self.base_url + '/?s=%22real+adventures%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Real Female Orgasms', self.base_url + '/?s=%22real+female+orgasms%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Rear View', self.base_url + '/?s=%22rear+view%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Roccos Dirty Dreams', self.base_url + '/?s=%22roccos+dirty+dreams%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Roccos Psycho Teens', self.base_url + '/?s=%22roccos+psycho+teens%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Rocco Ravishes', self.base_url + '/?s=%22rocco+ravishes%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Russian Angels', self.base_url + '/?s=%22russian+angels%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Screaming Assgasms', self.base_url + '/?s=%22screaming+assgasms%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Shades Of Kink', self.base_url + '/?s=%22shades+of+kink%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Slut Puppies', self.base_url + '/?s=%22Slut+Puppies%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Slutty And Sluttier', self.base_url + '/?s=%22slutty+and+sluttier%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Slutwoman', self.base_url + '/?s=slutwoman', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Squirt Gangbang', self.base_url + '/?s=%22squirt+gangbang%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Squirt Gasms', self.base_url + '/?s=%22squirt+gasms%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Stretch Class', self.base_url + '/?s=%22stretch+class%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Super Anal Cougars', self.base_url + '/?s=%22super+anal+cougars%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Teen America', self.base_url + '/?s=%22teen+america%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'The Sexual Desires Of', self.base_url + '/?s=%22the+sexual+desires+of%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Too Much Anal', self.base_url + '/?s=%22too+much+anal%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Top Wet Girls', self.base_url + '/?s=%22top+wet+girls%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Ultimate Fuck Toy', self.base_url + '/?s=%22ultimate+fuck+toy%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Up That White Ass', self.base_url + '/?s=%22up+that+white+ass%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'The Violation Of', self.base_url + '/?s=%22the+violation+of%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Voracious', self.base_url + '/?s=voracious', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Wet Asses', self.base_url + '/?s=%22wet+asses%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Young And Glamorous', self.base_url + '/?s=%22young+and+glamorous%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'Young Harlots', self.base_url + '/?s=%22young+harlots%22', indexer)

                '''
                self.AddSection(list, indexer, 'xsearch', 'xxx', self.base_url + '/?s=%22xxx%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'xxx', self.base_url + '/?s=%22xxx%22', indexer)
                self.AddSection(list, indexer, 'xsearch', 'xxx', self.base_url + '/?s=%22xxx%22', indexer)

                '''

            else:

                print 'presume ExtractContentAndAddtoList'
                print 'url ' + str(url)
                print 'type ' + type + '|page ' + page + '|total pages ' + total_pages + '|sort by ' + sort_by + '|sort order ' + sort_order

                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

    def GetFileHosts(self, url, list, lock, message_queue):
        print 'freeomovie ' + url
        print 'list ' + str(list)
        res = 'DVD'

        import re
        from entertainment.net import Net

        net = Net(cached=False)
        content = net.http_GET(url).content

        #print 'content ' + content.encode('utf-8')

        match=re.compile('<div class="videosection">\s(.+?)</div>',re.MULTILINE|re.DOTALL).findall(content)
        for entry in match:
            try:
                # Get the links out for new format pages
                breakout = re.compile('myURL\[\]=(.+?)["&]',re.MULTILINE|re.DOTALL).findall(entry)
                if len(breakout) == 0:
                    #old format?
                    breakout = re.compile('<a href="(.+?)"',re.MULTILINE|re.DOTALL).findall(entry)

                for url in breakout:
                    try:
                        import urlresolver
                        if urlresolver.HostedMediaFile(url).valid_url():
                            self.AddFileHost(list, quality=res, url=url)
                    except:
                        continue
            except:
                continue

        self.AddFileHost(list, quality=res, url=url)

    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        import re
        from entertainment.net import Net

        net = Net(cached=False)

        title = self.CleanTextForSearch(title)
        name = self.CleanTextForSearch(name)
        movie_url = self.base_url+'/'+name.lower().replace(' ','-')
        print 'movie_url ' + str(movie_url)
        content = net.http_GET(movie_url).content

        match=re.compile('<div class="videosection">\s(.+?)</div>',re.MULTILINE|re.DOTALL).findall(content)
        for entry in match:
            try:
                # Get the links out for new format pages
                breakout = re.compile('myURL\[\]=(.+?)["&]',re.MULTILINE|re.DOTALL).findall(entry)
                if len(breakout) == 0:
                    #old format?
                    breakout = re.compile('<a href="(.+?)"',re.MULTILINE|re.DOTALL).findall(entry)

                for url in breakout:
                    try:
                        import urlresolver
                        if urlresolver.HostedMediaFile(url).valid_url():
                            self.GetFileHosts(url, list, lock, message_queue)
                    except:
                        continue
            except:
                continue
