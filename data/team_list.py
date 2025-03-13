def get_team_logos():
    team_logos = {
        "Patriots": "https://loodibee.com/wp-content/uploads/nfl-new-england-patriots-team-logo-2.png",
        "Bills": "https://loodibee.com/wp-content/uploads/nfl-buffalo-bills-team-logo-2.png",
        "Jets": "https://loodibee.com/wp-content/uploads/New-York-Jets-logo-2024.png",
        "Dolphins": "https://loodibee.com/wp-content/uploads/nfl-miami-dolphins-team-logo-2.png",
        "Chiefs": "https://loodibee.com/wp-content/uploads/nfl-kansas-city-chiefs-team-logo-2.png",
        "Raiders": "https://loodibee.com/wp-content/uploads/nfl-oakland-raiders-team-logo.png",
        "Broncos": "https://loodibee.com/wp-content/uploads/nfl-denver-broncos-team-logo.png",
        "Chargers": "https://loodibee.com/wp-content/uploads/nfl-los-angeles-chargers-team-logo-2.png",
        "Ravens": "https://loodibee.com/wp-content/uploads/nfl-baltimore-ravens-team-logo-2.png",
        "Bengals": "https://loodibee.com/wp-content/uploads/nfl-cincinnati-bengals-team-logo.png",
        "Browns": "https://loodibee.com/wp-content/uploads/nfl-cleveland-browns-team-logo-2.png",
        "Steelers": "https://loodibee.com/wp-content/uploads/nfl-pittsburgh-steelers-team-logo-2.png",
        "Colts": "https://loodibee.com/wp-content/uploads/nfl-indianapolis-colts-team-logo-2.png",
        "Texans": "https://loodibee.com/wp-content/uploads/nfl-houston-texans-team-logo-2.png",
        "Jaguars": "https://loodibee.com/wp-content/uploads/nfl-jacksonville-jaguars-team-logo-2.png",
        "Titans": "https://loodibee.com/wp-content/uploads/nfl-tennessee-titans-team-logo-2.png",
        "Cowboys": "https://loodibee.com/wp-content/uploads/nfl-dallas-cowboys-team-logo-2.png",
        "Giants": "https://loodibee.com/wp-content/uploads/nfl-new-york-giants-team-logo-2.png",
        "Eagles": "https://loodibee.com/wp-content/uploads/nfl-philadelphia-eagles-team-logo-2.png",
        "Commanders": "https://loodibee.com/wp-content/uploads/washington-commanders-logo.png",
        "Redskins": "https://loodibee.com/wp-content/uploads/washington-commanders-logo.png", 
        "Packers": "https://loodibee.com/wp-content/uploads/nfl-green-bay-packers-team-logo-2.png",
        "Vikings": "https://loodibee.com/wp-content/uploads/nfl-minnesota-vikings-team-logo-2.png",
        "Bears": "https://loodibee.com/wp-content/uploads/nfl-chicago-bears-team-logo-2.png",
        "Lions": "https://loodibee.com/wp-content/uploads/nfl-detroit-lions-team-logo-2.png",
        "Saints": "https://loodibee.com/wp-content/uploads/nfl-new-orleans-saints-team-logo-2.png",
        "Buccaneers": "https://loodibee.com/wp-content/uploads/tampa-bay-buccaneers-2020-logo.png",
        "Falcons": "https://loodibee.com/wp-content/uploads/nfl-atlanta-falcons-team-logo-2.png",
        "Panthers": "https://loodibee.com/wp-content/uploads/nfl-carolina-panthers-team-logo-2.png",
        "49ers": "https://loodibee.com/wp-content/uploads/nfl-san-francisco-49ers-team-logo-2.png",
        "Seahawks": "https://loodibee.com/wp-content/uploads/nfl-seattle-seahawks-team-logo-2.png",
        "Rams": "https://loodibee.com/wp-content/uploads/los-angeles-rams-2020-logo.png",
        "Cardinals": "https://loodibee.com/wp-content/uploads/nfl-arizona-cardinals-team-logo-2.png",
    }
    return team_logos

def get_team_colors():
    team_colors = {
    'ARI': '#97233F', 'ATL': '#A71930', 'BAL': '#241773',
    'BUF': '#00338D', 'CAR': '#0085CA', 'CHI': '#0B162A',
    'CIN': '#FB4F14', 'CLE': '#311D00', 'DAL': '#041E42',
    'DEN': '#002244', 'DET': '#0076B6', 'GB': '#203731',
    'HOU': '#03202F', 'IND': '#002C5F', 'JAX': '#006778',
    'KC': '#E31837', 'LV': '#A5ACAF', 'LAC': '#0080C6',
    'LAR': '#003594', 'MIA': '#008E97', 'MIN': '#4F2683',
    'NE': '#002244', 'NO': '#D3BC8D', 'NYG': '#0B2265',
    'NYJ': '#125740', 'PHI': '#004C54', 'PIT': '#FFB612',
    'SF': '#AA0000', 'SEA': '#002244', 'TB': '#D50A0A',
    'TEN': '#4B92DB', 'WAS': '#773141'
    }
    return team_colors

def get_long_to_short_team_name_map():
    TEAM_NAME_MAP = {
    "Bills": "BUF",
    "Dolphins": "MIA",
    "Patriots": "NE",
    "Jets": "NYJ",
    "Ravens": "BAL",
    "Bengals": "CIN",
    "Browns": "CLE",
    "Steelers": "PIT",
    "Texans": "HOU",
    "Colts": "IND",
    "Jaguars": "JAX",
    "Titans": "TEN",
    "Oilers": "TEN",  # Houston Oilers → Tennessee Titans
    "Broncos": "DEN",
    "Chiefs": "KC",
    "Raiders": "LV",
    "Oakland Raiders": "LV",  # Oakland → Las Vegas
    "LA Raiders": "LV",  # LA Raiders → Las Vegas
    "Chargers": "LAC",
    "San Diego Chargers": "LAC",  # San Diego → LA
    "Cowboys": "DAL",
    "Giants": "NYG",
    "Eagles": "PHI",
    "Commanders": "WAS",
    "Washington Football Team": "WAS",  # Temporary name (2020-2021)
    "Redskins": "WAS",  
    "Bears": "CHI",
    "Lions": "DET",
    "Packers": "GB",
    "Vikings": "MIN",
    "Falcons": "ATL",
    "Panthers": "CAR",
    "Saints": "NO",
    "Buccaneers": "TB",
    "Cardinals": "ARI",
    "Rams": "LAR",
    "St. Louis Rams": "LAR",  # St. Louis → LA
    "49ers": "SF",
    "Seahawks": "SEA",
    }
    return TEAM_NAME_MAP

def get_short_to_long_team_abbreviation_map():
    TEAM_ABBREVIATION_MAP = {
        "BUF": "Bills",
        "MIA": "Dolphins",
        "NE": "Patriots",
        "NYJ": "Jets",
        "BAL": "Ravens",
        "CIN": "Bengals",
        "CLE": "Browns",
        "PIT": "Steelers",
        "HOU": "Texans",
        "IND": "Colts",
        "JAX": "Jaguars",
        "TEN": "Titans",
        "DEN": "Broncos",
        "KC": "Chiefs",
        "LV": "Raiders",
        "LAC": "Chargers",
        "DAL": "Cowboys",
        "NYG": "Giants",
        "PHI": "Eagles",
        "WAS": "Commanders",
        "CHI": "Bears",
        "DET": "Lions",
        "GB": "Packers",
        "MIN": "Vikings",
        "ATL": "Falcons",
        "CAR": "Panthers",
        "NO": "Saints",
        "TB": "Buccaneers",
        "ARI": "Cardinals",
        "LAR": "Rams",
        "SF": "49ers",
        "SEA": "Seahawks",
    }
    return TEAM_ABBREVIATION_MAP

def get_team_name_replacement_map():
    return {
        "Redskins": "Commanders",
        "Washington Football Team": "Commanders",
        "Oilers": "Titans",
        "St. Louis Rams": "Rams",
        "Oakland Raiders": "Raiders",
        "LA Raiders": "Raiders",
        "San Diego Chargers": "Chargers",
    }