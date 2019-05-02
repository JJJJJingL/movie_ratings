from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.stem import PorterStemmer
import string
from nltk.corpus import stopwords
from collections import Counter
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import pearsonr


# test_script = '/Users/ivywang/PycharmProjects/movie_ratings/script_file_upload.txt'


def preprocess(text, lower=False):
    tokens = word_tokenize(text)
    if lower:
        tokens = [token.lower() for token in tokens]
    ps = PorterStemmer()
    tokens_stemmed = [ps.stem(token) for token in tokens]
    # tokens_nopunc = [tok for tok in tokens_stemmed if tok not in string.punctuation]
    tokens_nostop = [tok for tok in tokens_stemmed if tok not in set(stopwords.words('english'))]

    return " ".join(tokens_nostop)


# this function makes a dictionary of all words in script, value is the word count
def word_count_all(list):
    # list is a
    all_word_count = {}
    all_words_list = []
    for script in list:
        word_list = preprocess(script).split()
        all_words_list.append(word_list)
    all_words_list = [item for sublist in all_words_list for item in sublist]
    for word in all_words_list:
        all_word_count[word] = all_word_count.get(word, 0) + 1
    return all_word_count


# calculate the mean number of word per utterane; takes the sum of all words in all utterance over number of utterance
def mean_words_per_sentence(script):
    #  script = """The constable's "responstable." Now, how does that sound?Hello, Miss Lark I got one for you.Miss Lark likes to walk in the park with Andrew.Your daughters were shorter than you, but they grew.Dear Miss Persimmon--Like something is brewin' about to beginCan't put me finger on what lies in storeBut I feel what's to happen, all happened before.And we'll sing in grateful chorus"Well done, Sister Suffragette"And dauntless crusaders for women's votesThough we adore men individuallyWe agree that as a group they're rather stupidShoulder to shoulder into the frayOur daughter's daughters will adore usAnd they'll sing in grateful chorus"Well done, Sister Suffragette"One hears the restless criesFrom every corner of the land: womankind arisePolitical equality and equal rights with menTake heart for Mrs. Pankhurst has been clapped in irons againNo more the meek and mild subservients weWe're fighting for our rights, militantly - never you fearOur daughter's daughters will adore usAnd they'll sing in grateful chorus - "well done"Much as a king astride his noble steed - thank you.When I return from daily strife, to hearth and wifeHow pleasant is the life I leadI run my home precisely on scheduleAt 6:01 I march through my doorMy slippers, sherry and pipe are due at 6:02Consistent is the life I leadIt's grand to be an Englishman in 1910King Edward's on the throne it's the age of menI'm the lord of my castle the sovereign, the liegeI treat my subjects, servants children, wife with a firm but gentle hand, noblesse obligeIt's 6:03 and the heirs to my dominionAre scrubbed and tubbed and adequately fedAnd so I'll pat them on the head and send them off to bedAh, lordly is the life I leadA British nanny must be a generalThe future empire lies within her handsAnd so the person that we needTo mold the breedIs a nanny who can give commandsA British bank is run with precisionA British home requires nothing lessTradition, discipline and rules must be the toolsWithout them, disorder, catastrophe, anarchyIn short you have a ghastly messIf you want this choice positionHave a cheery dispositionPlay games, all sortsYou must be kind you must be wittyVery sweet and fairly prettyTake us on outings give us treatsSing songs bring sweetsNever be cross or cruel never give us castor oil or gruelLove us as a son and daughterAnd never smell of barley waterIf you won't scold and dominate usWe will never you give you cause to hate usWe won't hide your spectacles so you can't seePut toads in your bed or pepper in your teaHurry, nannyMany thanksSincerelyThere is an element of fun.You find the fun, and snap!The job's a game.And every task you undertakeBecomes a piece of cakeA lark, a spree it's very clear to seeThat a spoonful of sugar helps the medicine go downThe medicine go downMedicine go downJust a spoonful of sugar helps the medicine go downIn a most delightful wayA robin feathering his nestHas very little time to restWhile gathering his bits of twine and twigThough quite intent in his pursuit,He has a merry tune to tootHe knows a song will move the job alongFor a spoonful of sugar helps the medicine go downThe medicine go downMedicine go downJust a spoonful of sugar helps the medicine go downIn a most delightful wayThe honeybees that fetch the nectar from the flowers to the combNever tire of ever buzzing to and froBecause they take a little nip from every flower that they sipAnd henceAnd henceThey findTheir task is not a grindFor a spoonful of sugar helps the medicine go downThe medicine go downMedicine go downJust a spoonful of sugar helps the medicineGo down in the most delightful wayI does what I likes and I likes what I doToday I'm a screever and as you can seeA screever's an artist of highest degreeAnd it's all me own workFrom me own memoryChim chiminy, chim chiminy chim chim cherooI draws what I likes and I likes what I drewNo remuneration do I ask of youBut me cap would be glad of a copper or twoMe cap would be glad of a copper or twoRight as a mornin' in MayI feel like I could flyHave you ever seenThe grass so greenOr a bluer skyOh, it's a jolly holiday with MaryMary makes your heart so lightWhen the day is gray and ordinaryMary makes the sun shine brightOh, happiness is bloomin' all around herThe daffodils are smilin' at the doveWhen Mary holds your hand you feel so grandYour heart starts beatin' like a big brass bandNo wonder that it's Mary that we loveOh, it's a jolly holiday with MaryMary makes your heart so lightWhen the day is gray and ordinaryMary makes the sun shine brightOh, happiness is bloomin' all around herThe daffodils are smiling at the dove oink, oink.When Mary holds your handYou feel so grandYour heart starts beatin' like a big brass bandIt's a jolly holiday with MaryNo wonder that it's Mary that we loveOh, it's a jolly holiday with you, BertGentlemen like you are fewThough you're just a diamond in the rough, BertUnderneath your blood is blueYou'd never think of pressing your advantageForbearance is the hallmark of your creedA lady needn't fearWhen you are nearYour sweet gentility is crystal clearOh, it's a jolly holiday with you, BertA jolly, jolly holiday with youWe'll start with raspberry iceand then some cakes and teaOrder what you willThere'll be no billIt's complimentaryWhen Mary holds your handYou feel so grandYour heart starts beatin' like a big brass bandIt's a jolly holiday with MaryNo wonder that it's Mary that we loveNo wonder that it's Mary that we loveNo wonder that it's Mary that we loveEven though the sound of it is something quite atrociousIf you say it loud enough you'll always sound precociousSupercalifragilistic- expialidociousUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle ayBecause I was afraid to speak when I was just a ladMe father gave me nose a tweak and told me I was badBut then one day I learned a word that saved me achin' noseThe biggest word you ever heard and this is how it goesOh, supercalifragilistic- expialidociousEven though the sound of it is something quite atrociousIf you say it loud enough you'll always sound precociousSupercalifragilistic- expialidociousUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle ayHe's traveled all around the world and everywhere he wentHe'd use his word and all would say, "there goes a clever gent"When dukes and maharajahs pass the time of day with meI'd say me special word and then they'd ask me out to teaOoh, supercalifragilistic- expialidociousEven though the sound of it is something quite atrociousIf you say it loud enough you'll always sound precociousSupercalifragilistic- expialidociousUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle aySo when the cat has got your tongue there's no need for dismayJust summon up this word and then you've got a lot to sayShe's supercalifragilistic- expialidociousSupercalifragilistic- expialidociousSupercalifragilistic- expialidociousSupercalifragilistic-expialidociousChim chiminy, chim chiminy chim chim cherooLa dum da da dum da da da da dumDon't lie down upon your bedWhile the moon drifts in the skiesStay awake don't close your eyesThough the world is fast asleepThough your pillow's soft and deepYou're not sleepy as you seemStay awake don't nod and dreamStay awake don't nod and dreamSupercalifragilistic- expialidociousSupercalifragilistic-expialidociousSupercalifragilistic- expialidociousSupercalifragilistic- expialidociousSupercalifragilistic- expialidociousI love to laughLoud and long and clearI love to laughIt's getting worse every yearThe more I laughThe more I fill with gleeThe more the gleeThe more I'm a merrier meThe more I'm a merrier meSome people laugh through their nosesSounding something like this -- dreadful!Some people laugh through their teeth, goodness sakesHissing and fizzing like snakesSome laugh too fastSome only blastOthers, they twitter like birdsAnd squeak as the squeakelers doI've got to let go with a ho ho ho hoAnd laugh tooWe love to laughLoud and long and clearWe love to laughSo everybody can hearThe more you laughThe more you fill with gleeThe more the gleeThe more we're a merrier weA British home requires nothing lessTradition, discipline and rulesMust be the toolsWithout them disorder, chaos, moral disintegrationIn short you have a ghastly messThat life's a looming battle to be faced and foughtIf they must go on outingsThese outings ought to beAnd popping through picturesHave little use, fulfill no basic needThey've got to learn the honest truthDespite their youthThey must learnThey must feel the thrill of totting up a balanced bookA thousand ciphers neatly in a rowWhen gazing at a graph that shows the profits upTheir little cup of joy should overflowTomorrow just as you suggestPressed and dressedJane and Michael will be at your sideEarly each day to the steps of St. Paul'sThe little old bird woman comesIn her own special way to the people she callsCome buy my bags full of crumbsCome feed the little birds show them you careAnd you'll be glad if you doTheir young ones are hungryTheir nests are so bareAll it takes is tuppence from youFeed the birds tuppence a bagTuppence, tuppence tuppence a bagFeed the birds that's what she criesWhile overhead her birds fill the skiesAll around the cathedralThe saints and apostlesLook down as she sells her waresAlthough you can't see itYou know they are smilingEach time someone shows that he caresThough her words are simple and fewListen, listen she's calling to youFeed the birds tuppence a bagTuppence, tuppence tuppence a bagThough her words are simple and fewListen, listen she's calling to youFeed the birds tuppence a bagTuppence, tuppence tuppence a bagBut if you invest your tuppenceWisely in the bankSafe and soundSoon that tuppence safely invested in the bankWill compoundAnd you'll achieve that sense of conquestAs your affluence expandsIn the hands of the directorsWho invest as propriety demandsMajestic self-amortizing canalsPlantations of ripening tea all fromTuppence prudently thriftily, frugallyInvested in theIn the Dawes, Tomes Mousley, Grubbs, Fidelity Fiduciary BankThat it blooms into credit of a generous amount semi-annuallyAnd you'll achieve that sense of statureAs your influence expandsTo the high financial strataThat established credit now commandsTuppence patiently, cautiously trustingly invested in theTo be specific in the Dawes, Tomes, Mousley, Grubbs, Fidelity Fiduciary BankChim chiminy, chim chiminy chim chim chereeA sweep is as lucky as lucky can beChim chiminy, chim chiminy chim chim cherooGood luck will rub off when I shakes hands with youOr blow me a kiss and that's lucky tooNow as the ladder of life has been strungYou might think a sweep's on the bottommost rungThough I spends me time in the ashes and smokeIn this whole wide world there's no happier blokeChim chiminy, chim chiminy chim chim chereeA sweep is as lucky as lucky can beChim chiminy, chim chiminy chim chim cherooGood luck will rub off when I shakes hands with youChim chiminy, chim chiminy chim chim chereeA sweep is as lucky as lucky can beChim chiminy, chim chiminy chim chim cherooGood luck will rub off when I shakes hands with youI choose me bristles with pride, yes, I doA broom for the shaftAnd a brush for the flue'Tween pavement and starsIs the chimney sweep worldWhen there's hardly no dayNor hardly no nightThere's things half in shadowAnd halfway in lightOn the rooftops of LondonCoo, what a sight.Chim chiminy, chim chiminy chimChim cheree when you're with a sweep you're in glad companyThan them what sings chim chim cheree, chim cherooChim chiminy chim chim cheree chim cherooStep in time!Step in time!Step in time!Step in time!Step in time!Step in time, step in timeCome on, mateys, step in timeStep in timeStep in time,Step in timeStep in time,Step in timeNever need a reason never need a rhymeWe step in time, we step in timeKick your knees up step in timeKick your knees up, step in timeNever need a reason never need a rhymeKick your knees up step in timeRound the chimney step in timeRound the chimney, step in timeNever need a reason never need a rhymeRound the chimney we step in timeClap like a birdie step in timeClap like a birdie, step in timeNever need a reason never need a rhymeClap like a birdie in timeUp on the railing step in timeUp on the railing, step in timeNever need a reason never need a rhyme upOn the railing step in timeOver the rooftops step in timeOver the rooftops, step in timeNever need a reason never need a rhymeStep it time,Over the rooftopsOver the rooftopsLink your elbows, step in timeLink your elbows, step in timeLink your elbows,Link your elbows,Link your elbowsStep in time,Step in timeStep in time,Step in timeNever need a reason never need a rhymeWhen you step in time you step in timeThey're at it again!Step it time,At it againStep in timeThey're at it againStep it time ow!Ow,Step in timeOw,Step in timeNever need a reason never need a rhymeWhoa!Step in timeVotes for women, step in timeVotes for women, step in timeVotes for womenVotes for women!It's the master,Step in timeIt's the master, step in timeWhat's all thisWhat's all this?What's all thisWhat's all thisWhat's all thisWhat's all thisLink your elbows, step in timeWhat's all this?Kick your knees up what's all this?Step in timeKick your knees upKick your knees up Bert.Kick your knees upKick your knees up in timeA man has dreams of walking with giants.To carve his niche in the edifice of time.Before the mortar of his zealHas a chance to congealThe cup is dashed from his lips!The flame is snuffed a-borning.He's brought to wrack and ruin in his prime.My world was calm, well-ordered, exemplary.Then came this person with chaos in her wakeAnd now my life's ambitions goWith one fell blowA spoonful of sugar that is all it takesIt changes bread and water into tea and cakesA spoonful of sugar goes a long, long wayHave yourself a healthy helpin' everydayAnd when your little tykes are cryin' you haven't time to dry their tearsand see them grateful little faces smilin' up at youbecause their dad he always knows just what to doYou've got to grind, grind, grind at that grindstoneThough childhood slips like sand through a sieveAnd all too soon they've up and grownAnd then they've flownAnd it's too late for you to giveJust that spoonful of sugar to help the medicine go downThe medicine go downMedicine go downA spoonful of sugar makes the medicine go downThe medicine go downThe medicine go downThe medicine--The medicine go downThe medicine go downJust a spoonful of sugarWith tuppence for paper and stringsYou can have your own set of wingsWith your feet on the groundYou're a bird in flightWith your fist holding tightTo the string of your kiteOh, oh, ohLet's go fly a kiteUp to the highest heightLet's go fly a kiteAnd send it soaringUp through the atmosphereUp where the air is clearOh, let's go fly a kiteLet's go fly a kiteUp to the highest heightLet's go fly a kite and send it soaringUp through the atmosphereUp where the air is clearOh, let's go fly a kiteWhen you send it flying up thereAll at once you're lighter than airYou can dance on the breezeOver houses and treesWith your fist holding tightTo the string of your kiteOh, oh, ohLet's go fly a kiteUp to the highest heightLet's go fly a kite and send it soaringUp through the atmosphereUp where the air is clearOh, let's go fly a kite"""
    utterances = sent_tokenize(script)
    # the number of sentences in this script
    number_utterances = len(utterances)
    sum_num_words = 0
    #  num_words =[]
    for sent in utterances:
        sent_tokens = word_tokenize(sent)
        #     num_words.append(len(sent_tokens))
        sum_num_words += len(sent_tokens)

    mean = sum_num_words / number_utterances
    #    print(utterances)
    #    print(mean)
    return utterances, mean, number_utterances


def add_pos_tag(script):
    #   script = """The constable's "responstable." Now, how does that sound?Hello, Miss Lark I got one for you.Miss Lark likes to walk in the park with Andrew.Your daughters were shorter than you, but they grew.Dear Miss Persimmon--Like something is brewin' about to beginCan't put me finger on what lies in storeBut I feel what's to happen, all happened before.And we'll sing in grateful chorus"Well done, Sister Suffragette"And dauntless crusaders for women's votesThough we adore men individuallyWe agree that as a group they're rather stupidShoulder to shoulder into the frayOur daughter's daughters will adore usAnd they'll sing in grateful chorus"Well done, Sister Suffragette"One hears the restless criesFrom every corner of the land: womankind arisePolitical equality and equal rights with menTake heart for Mrs. Pankhurst has been clapped in irons againNo more the meek and mild subservients weWe're fighting for our rights, militantly - never you fearOur daughter's daughters will adore usAnd they'll sing in grateful chorus - "well done"Much as a king astride his noble steed - thank you.When I return from daily strife, to hearth and wifeHow pleasant is the life I leadI run my home precisely on scheduleAt 6:01 I march through my doorMy slippers, sherry and pipe are due at 6:02Consistent is the life I leadIt's grand to be an Englishman in 1910King Edward's on the throne it's the age of menI'm the lord of my castle the sovereign, the liegeI treat my subjects, servants children, wife with a firm but gentle hand, noblesse obligeIt's 6:03 and the heirs to my dominionAre scrubbed and tubbed and adequately fedAnd so I'll pat them on the head and send them off to bedAh, lordly is the life I leadA British nanny must be a generalThe future empire lies within her handsAnd so the person that we needTo mold the breedIs a nanny who can give commandsA British bank is run with precisionA British home requires nothing lessTradition, discipline and rules must be the toolsWithout them, disorder, catastrophe, anarchyIn short you have a ghastly messIf you want this choice positionHave a cheery dispositionPlay games, all sortsYou must be kind you must be wittyVery sweet and fairly prettyTake us on outings give us treatsSing songs bring sweetsNever be cross or cruel never give us castor oil or gruelLove us as a son and daughterAnd never smell of barley waterIf you won't scold and dominate usWe will never you give you cause to hate usWe won't hide your spectacles so you can't seePut toads in your bed or pepper in your teaHurry, nannyMany thanksSincerelyThere is an element of fun.You find the fun, and snap!The job's a game.And every task you undertakeBecomes a piece of cakeA lark, a spree it's very clear to seeThat a spoonful of sugar helps the medicine go downThe medicine go downMedicine go downJust a spoonful of sugar helps the medicine go downIn a most delightful wayA robin feathering his nestHas very little time to restWhile gathering his bits of twine and twigThough quite intent in his pursuit,He has a merry tune to tootHe knows a song will move the job alongFor a spoonful of sugar helps the medicine go downThe medicine go downMedicine go downJust a spoonful of sugar helps the medicine go downIn a most delightful wayThe honeybees that fetch the nectar from the flowers to the combNever tire of ever buzzing to and froBecause they take a little nip from every flower that they sipAnd henceAnd henceThey findTheir task is not a grindFor a spoonful of sugar helps the medicine go downThe medicine go downMedicine go downJust a spoonful of sugar helps the medicineGo down in the most delightful wayI does what I likes and I likes what I doToday I'm a screever and as you can seeA screever's an artist of highest degreeAnd it's all me own workFrom me own memoryChim chiminy, chim chiminy chim chim cherooI draws what I likes and I likes what I drewNo remuneration do I ask of youBut me cap would be glad of a copper or twoMe cap would be glad of a copper or twoRight as a mornin' in MayI feel like I could flyHave you ever seenThe grass so greenOr a bluer skyOh, it's a jolly holiday with MaryMary makes your heart so lightWhen the day is gray and ordinaryMary makes the sun shine brightOh, happiness is bloomin' all around herThe daffodils are smilin' at the doveWhen Mary holds your hand you feel so grandYour heart starts beatin' like a big brass bandNo wonder that it's Mary that we loveOh, it's a jolly holiday with MaryMary makes your heart so lightWhen the day is gray and ordinaryMary makes the sun shine brightOh, happiness is bloomin' all around herThe daffodils are smiling at the dove oink, oink.When Mary holds your handYou feel so grandYour heart starts beatin' like a big brass bandIt's a jolly holiday with MaryNo wonder that it's Mary that we loveOh, it's a jolly holiday with you, BertGentlemen like you are fewThough you're just a diamond in the rough, BertUnderneath your blood is blueYou'd never think of pressing your advantageForbearance is the hallmark of your creedA lady needn't fearWhen you are nearYour sweet gentility is crystal clearOh, it's a jolly holiday with you, BertA jolly, jolly holiday with youWe'll start with raspberry iceand then some cakes and teaOrder what you willThere'll be no billIt's complimentaryWhen Mary holds your handYou feel so grandYour heart starts beatin' like a big brass bandIt's a jolly holiday with MaryNo wonder that it's Mary that we loveNo wonder that it's Mary that we loveNo wonder that it's Mary that we loveEven though the sound of it is something quite atrociousIf you say it loud enough you'll always sound precociousSupercalifragilistic- expialidociousUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle ayBecause I was afraid to speak when I was just a ladMe father gave me nose a tweak and told me I was badBut then one day I learned a word that saved me achin' noseThe biggest word you ever heard and this is how it goesOh, supercalifragilistic- expialidociousEven though the sound of it is something quite atrociousIf you say it loud enough you'll always sound precociousSupercalifragilistic- expialidociousUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle ayHe's traveled all around the world and everywhere he wentHe'd use his word and all would say, "there goes a clever gent"When dukes and maharajahs pass the time of day with meI'd say me special word and then they'd ask me out to teaOoh, supercalifragilistic- expialidociousEven though the sound of it is something quite atrociousIf you say it loud enough you'll always sound precociousSupercalifragilistic- expialidociousUm diddle diddle diddle um diddle ayUm diddle diddle diddle um diddle aySo when the cat has got your tongue there's no need for dismayJust summon up this word and then you've got a lot to sayShe's supercalifragilistic- expialidociousSupercalifragilistic- expialidociousSupercalifragilistic- expialidociousSupercalifragilistic-expialidociousChim chiminy, chim chiminy chim chim cherooLa dum da da dum da da da da dumDon't lie down upon your bedWhile the moon drifts in the skiesStay awake don't close your eyesThough the world is fast asleepThough your pillow's soft and deepYou're not sleepy as you seemStay awake don't nod and dreamStay awake don't nod and dreamSupercalifragilistic- expialidociousSupercalifragilistic-expialidociousSupercalifragilistic- expialidociousSupercalifragilistic- expialidociousSupercalifragilistic- expialidociousI love to laughLoud and long and clearI love to laughIt's getting worse every yearThe more I laughThe more I fill with gleeThe more the gleeThe more I'm a merrier meThe more I'm a merrier meSome people laugh through their nosesSounding something like this -- dreadful!Some people laugh through their teeth, goodness sakesHissing and fizzing like snakesSome laugh too fastSome only blastOthers, they twitter like birdsAnd squeak as the squeakelers doI've got to let go with a ho ho ho hoAnd laugh tooWe love to laughLoud and long and clearWe love to laughSo everybody can hearThe more you laughThe more you fill with gleeThe more the gleeThe more we're a merrier weA British home requires nothing lessTradition, discipline and rulesMust be the toolsWithout them disorder, chaos, moral disintegrationIn short you have a ghastly messThat life's a looming battle to be faced and foughtIf they must go on outingsThese outings ought to beAnd popping through picturesHave little use, fulfill no basic needThey've got to learn the honest truthDespite their youthThey must learnThey must feel the thrill of totting up a balanced bookA thousand ciphers neatly in a rowWhen gazing at a graph that shows the profits upTheir little cup of joy should overflowTomorrow just as you suggestPressed and dressedJane and Michael will be at your sideEarly each day to the steps of St. Paul'sThe little old bird woman comesIn her own special way to the people she callsCome buy my bags full of crumbsCome feed the little birds show them you careAnd you'll be glad if you doTheir young ones are hungryTheir nests are so bareAll it takes is tuppence from youFeed the birds tuppence a bagTuppence, tuppence tuppence a bagFeed the birds that's what she criesWhile overhead her birds fill the skiesAll around the cathedralThe saints and apostlesLook down as she sells her waresAlthough you can't see itYou know they are smilingEach time someone shows that he caresThough her words are simple and fewListen, listen she's calling to youFeed the birds tuppence a bagTuppence, tuppence tuppence a bagThough her words are simple and fewListen, listen she's calling to youFeed the birds tuppence a bagTuppence, tuppence tuppence a bagBut if you invest your tuppenceWisely in the bankSafe and soundSoon that tuppence safely invested in the bankWill compoundAnd you'll achieve that sense of conquestAs your affluence expandsIn the hands of the directorsWho invest as propriety demandsMajestic self-amortizing canalsPlantations of ripening tea all fromTuppence prudently thriftily, frugallyInvested in theIn the Dawes, Tomes Mousley, Grubbs, Fidelity Fiduciary BankThat it blooms into credit of a generous amount semi-annuallyAnd you'll achieve that sense of statureAs your influence expandsTo the high financial strataThat established credit now commandsTuppence patiently, cautiously trustingly invested in theTo be specific in the Dawes, Tomes, Mousley, Grubbs, Fidelity Fiduciary BankChim chiminy, chim chiminy chim chim chereeA sweep is as lucky as lucky can beChim chiminy, chim chiminy chim chim cherooGood luck will rub off when I shakes hands with youOr blow me a kiss and that's lucky tooNow as the ladder of life has been strungYou might think a sweep's on the bottommost rungThough I spends me time in the ashes and smokeIn this whole wide world there's no happier blokeChim chiminy, chim chiminy chim chim chereeA sweep is as lucky as lucky can beChim chiminy, chim chiminy chim chim cherooGood luck will rub off when I shakes hands with youChim chiminy, chim chiminy chim chim chereeA sweep is as lucky as lucky can beChim chiminy, chim chiminy chim chim cherooGood luck will rub off when I shakes hands with youI choose me bristles with pride, yes, I doA broom for the shaftAnd a brush for the flue'Tween pavement and starsIs the chimney sweep worldWhen there's hardly no dayNor hardly no nightThere's things half in shadowAnd halfway in lightOn the rooftops of LondonCoo, what a sight.Chim chiminy, chim chiminy chimChim cheree when you're with a sweep you're in glad companyThan them what sings chim chim cheree, chim cherooChim chiminy chim chim cheree chim cherooStep in time!Step in time!Step in time!Step in time!Step in time!Step in time, step in timeCome on, mateys, step in timeStep in timeStep in time,Step in timeStep in time,Step in timeNever need a reason never need a rhymeWe step in time, we step in timeKick your knees up step in timeKick your knees up, step in timeNever need a reason never need a rhymeKick your knees up step in timeRound the chimney step in timeRound the chimney, step in timeNever need a reason never need a rhymeRound the chimney we step in timeClap like a birdie step in timeClap like a birdie, step in timeNever need a reason never need a rhymeClap like a birdie in timeUp on the railing step in timeUp on the railing, step in timeNever need a reason never need a rhyme upOn the railing step in timeOver the rooftops step in timeOver the rooftops, step in timeNever need a reason never need a rhymeStep it time,Over the rooftopsOver the rooftopsLink your elbows, step in timeLink your elbows, step in timeLink your elbows,Link your elbows,Link your elbowsStep in time,Step in timeStep in time,Step in timeNever need a reason never need a rhymeWhen you step in time you step in timeThey're at it again!Step it time,At it againStep in timeThey're at it againStep it time ow!Ow,Step in timeOw,Step in timeNever need a reason never need a rhymeWhoa!Step in timeVotes for women, step in timeVotes for women, step in timeVotes for womenVotes for women!It's the master,Step in timeIt's the master, step in timeWhat's all thisWhat's all this?What's all thisWhat's all thisWhat's all thisWhat's all thisLink your elbows, step in timeWhat's all this?Kick your knees up what's all this?Step in timeKick your knees upKick your knees up Bert.Kick your knees upKick your knees up in timeA man has dreams of walking with giants.To carve his niche in the edifice of time.Before the mortar of his zealHas a chance to congealThe cup is dashed from his lips!The flame is snuffed a-borning.He's brought to wrack and ruin in his prime.My world was calm, well-ordered, exemplary.Then came this person with chaos in her wakeAnd now my life's ambitions goWith one fell blowA spoonful of sugar that is all it takesIt changes bread and water into tea and cakesA spoonful of sugar goes a long, long wayHave yourself a healthy helpin' everydayAnd when your little tykes are cryin' you haven't time to dry their tearsand see them grateful little faces smilin' up at youbecause their dad he always knows just what to doYou've got to grind, grind, grind at that grindstoneThough childhood slips like sand through a sieveAnd all too soon they've up and grownAnd then they've flownAnd it's too late for you to giveJust that spoonful of sugar to help the medicine go downThe medicine go downMedicine go downA spoonful of sugar makes the medicine go downThe medicine go downThe medicine go downThe medicine--The medicine go downThe medicine go downJust a spoonful of sugarWith tuppence for paper and stringsYou can have your own set of wingsWith your feet on the groundYou're a bird in flightWith your fist holding tightTo the string of your kiteOh, oh, ohLet's go fly a kiteUp to the highest heightLet's go fly a kiteAnd send it soaringUp through the atmosphereUp where the air is clearOh, let's go fly a kiteLet's go fly a kiteUp to the highest heightLet's go fly a kite and send it soaringUp through the atmosphereUp where the air is clearOh, let's go fly a kiteWhen you send it flying up thereAll at once you're lighter than airYou can dance on the breezeOver houses and treesWith your fist holding tightTo the string of your kiteOh, oh, ohLet's go fly a kiteUp to the highest heightLet's go fly a kite and send it soaringUp through the atmosphereUp where the air is clearOh, let's go fly a kite"""

    text = word_tokenize(script)
    total_words = len(text)
    script_tagged = pos_tag(text)
    num_noun = 0
    num_adj = 0
    num_verb = 0
    for token, tag in script_tagged:
        if tag.startswith('N'):
            num_noun += 1
        if tag.startswith('J'):
            num_adj += 1
        if tag.startswith('V'):
            num_verb += 1

    percentage_n = num_noun / total_words
    percentage_adj = num_adj / total_words
    percentage_v = num_verb / total_words

    return percentage_n, percentage_adj, percentage_v

mean_list = []
baseline_list = []
percentage_n_list = []
percentage_a_list = []
percentage_v_list = []
script_list = []
rating_list = []
# make vector
# read cleaned data into list
with open('script_file.txt', 'r') as scripts_file:
    file = scripts_file.readlines()
    for line in file:
        fields = line.split('\t')
        rating_list.append(float(fields[1]))
        script = fields[2]
        script_list.append(script)  # script list is the script
        temp_n, temp_a, temp_v = add_pos_tag(script)
        percentage_n_list.append(temp_n)
        percentage_a_list.append(temp_a)
        percentage_v_list.append(temp_v)
        baseline_list.append(number_sent)
        utterances, mean, number_sent = mean_words_per_sentence(script)
        if mean < 50:
            mean_list.append(mean)
        else:
            mean_list.append(0)


# Due to the punctuation variation of original scripts, we need to exclude the mean > 100, and correspondingly, get rid of these items in all of the other feature list
# 890-> 824


script_list_stripped = [script for i, script in enumerate(script_list) if mean_list[i] is not 0] # 824
mean_list_stripped = [mean for mean in mean_list if mean is not 0]
rating_list_stripped = [rating for i, rating in enumerate(rating_list) if mean_list[i] is not 0]
baseline_list_stripped = [b for i, b in enumerate(baseline_list) if mean_list[i] is not 0]
percentage_a_list_str = [b for i, b in enumerate(percentage_a_list) if mean_list[i] is not 0]
percentage_n_list_str = [b for i, b in enumerate(percentage_n_list) if mean_list[i] is not 0]
percentage_v_list_str = [b for i, b in enumerate(percentage_v_list) if mean_list[i] is not 0]

mean_array = np.asarray(mean_list_stripped)  # this is feature array for mean
# print(mean_array)
X_mean = mean_array.reshape(-1, 1)

vectorizer = TfidfVectorizer("content", lowercase=True, analyzer="word", use_idf=True, min_df=10)
vectorizer.fit(script_list_stripped)
tfidf_list = []
# X_tfidf = np.asarray(tfidf_list)
for script in script_list_stripped:
    script_vector = vectorizer.transform([script])
    tfidf = script_vector.toarray()
    tfidf_list.append(tfidf)
    # print(tfidf)
X_tfidf = np.vstack(tfidf_list)
print(X_tfidf.shape)
print(X_mean.shape)

X_tfidf_mean = np.column_stack((X_mean, X_tfidf))

y = np.asarray(rating_list_stripped)
y = y.reshape(-1,1)
X_mean = X_mean.reshape(-1, 1)

print(y.shape)
# baseline: number of sentences
X_base = np.asarray(baseline_list_stripped).reshape(-1, 1)
print(X_base.shape)
X_pos_a = np.asarray(percentage_a_list_str)
X_pos_n = np.asarray(percentage_n_list_str)
X_pos_v = np.asarray(percentage_v_list_str)
X_all = np.column_stack((X_mean, X_tfidf, X_pos_v, X_pos_a, X_pos_n))
X_pos = np.column_stack((X_pos_a, X_pos_n, X_pos_v))

# baseline model fitting
# model = RandomForestRegressor(n_estimators=10, random_state=42)
# fitted = model.fit(train_X, train_y)
# predicted = model.predict(val_X)
#
# # print(predicted)
# error = abs(predicted - val_y)
# print(round(np.mean(error), 2))
#
# # Calculate mean absolute percentage error (MAPE)
# mape = 100 * (error / val_y)
# # Calculate and display accuracy
# accuracy = 100 - np.mean(mape)
# print('Model with number of sentences accuracy:', round(accuracy, 2), '%.')

# tdidf model fitting


# # make model
# model = RandomForestRegressor(n_estimators=10, random_state=42)
# fitted = model.fit(train_X, train_y)
# predicted = model.predict(val_X)
#
# print(predicted)
# error = abs(predicted - val_y)
# print(round(np.mean(error), 2))
#
# # Calculate mean absolute percentage error (MAPE)
# mape = 100 * (error / val_y)
# # Calculate and display accuracy
# accuracy = 100 - np.mean(mape)
# print('Model with tfidf accuracy:', round(accuracy, 2), '%.')
#
# # mean of length per sentence model fitting
# train_X, test_X, train_y, test_y = train_test_split(X_mean, y, test_size=0.2)
# train_X, val_X, train_y, val_y = train_test_split(train_X, train_y, test_size=0.2)

# model = RandomForestRegressor(n_estimators=1000, random_state=42)
# fitted = model.fit(train_X, train_y)
# predicted = model.predict(val_X)
# print(predicted)
# # print(predicted)
# error = abs(predicted - val_y)
# print(round(np.mean(error), 2))
#
# # Calculate mean absolute percentage error (MAPE)
# mape = 100 * (error / val_y)
# # Calculate and display accuracy
# accuracy = 100 - np.mean(mape)
# print('Model with mean words per sentence accuracy:', round(accuracy, 2), '%.')
#
# # baseline with two features (tfidf + mean of the length per sentence) model fitting
#
# model = RandomForestRegressor(n_estimators=10, random_state=42)
# fitted = model.fit(train_X, train_y)
# predicted = model.predict(val_X)
#
# # print(predicted)
# error = abs(predicted - val_y)
# print(round(np.mean(error), 2))
#
# # Calculate mean absolute percentage error (MAPE)
# mape = 100 * (error / val_y)
# # Calculate and display accuracy
# accuracy = 100 - np.mean(mape)
# print('tfidf+ mean words per sentence accuracy:', round(accuracy, 2), '%.')
#

train_X_tfidf_mean, test_X_tfidf_mean, train_y, test_y = train_test_split(X_tfidf_mean, y, test_size=0.2)
train_X_tfidf_mean, val_X_tfidf_mean, train_y, val_y = train_test_split(train_X_tfidf_mean, train_y, test_size=0.2)

train_X_all, test_X_all, train_y, test_y = train_test_split(X_all, y, test_size=0.2)
train_X_all, val_X_all, train_y, val_y = train_test_split(train_X_all, train_y, test_size=0.2)

train_X_pos, test_X_pos, train_y, test_y = train_test_split(X_pos, y, test_size=0.2)
train_X_pos, val_X_pos, train_y, val_y = train_test_split(train_X_pos, train_y, test_size=0.2)

train_X_tfidf, test_X_tfidf, train_y, test_y = train_test_split(X_tfidf, y, test_size=0.2)
train_X_tfidf, val_X_tfidf, train_y, val_y = train_test_split(train_X_tfidf, train_y, test_size=0.2)

train_X_mean, test_X_mean, train_y, test_y = train_test_split(X_mean, y, test_size=0.2)
train_X_mean, val_X_mean, train_y, val_y = train_test_split(train_X_mean, train_y, test_size=0.2)


train_X_base, test_X_base, train_y, test_y = train_test_split(X_base, y, test_size=0.2)
train_X_base, val_X_base, train_y, val_y = train_test_split(train_X_base, train_y, test_size=0.2)

def random_forest(train_X, train_y, val_X, val_y):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(train_X, train_y)
    predicted = model.predict(val_X).reshape(-1,1)
    # print(predicted)
    error = abs(predicted - val_y)
    # print(round(np.mean(error), 2))
    # Calculate mean absolute percentage error (MAPE)
    mape = 100 * (error / val_y)
    # Calculate and display accuracy
    accuracy = 100 - np.mean(mape)
    print('mean words + number of sentences accuracy:', round(accuracy, 5), '%.')
    forest_corr, p_value = pearsonr(predicted, val_y)
    print(forest_corr)
    return accuracy, forest_corr

# linear regression
def linear_model(train_X, train_y, val_X, val_y):
    model_linear_mean = LinearRegression()
    model_linear_mean.fit(train_X, train_y)
    predicted_linear = model_linear_mean.predict(val_X)
    score_linear = model_linear_mean.score(val_X, val_y)
    print(score_linear)
    correlation_linear, p_value = pearsonr(predicted_linear, val_y)
    print(correlation_linear)
    return score_linear, correlation_linear

linear_model_score, pearson_corr = linear_model(train_X_all, train_y, val_X_all, val_y)
# accuracy score: -0.18 TFIDF, 0.0025 baseline, -0.01028 mean
# pearson corr: [0.15177801] base, 0.15341161 tfidf, 0.0351 mean,

forest_accuracy, forest_corr = random_forest(train_X_all, train_y, val_X_all, val_y)