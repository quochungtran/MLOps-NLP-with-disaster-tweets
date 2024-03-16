from src.text_preprocessing import get_substitutions
from src.text_preprocessing import cleaning_text
from src.text_preprocessing import remove_urls
from src.text_preprocessing import remove_punc
from src.text_preprocessing import processing_text

import src.config as cfg
import os
import pandas as pd
from pandas.testing import assert_frame_equal

def test_remove_urls():
    org_text_1      = "Check out this link: http://t.co/2nndBGwyEi"
    excepted_text_1 = "Check out this link: "

    assert remove_urls(org_text_1) == excepted_text_1

    org_text_2      = "@bbcmtd Wholesale Markets ablaze http://t.co/lHYXEOHY6C"
    excepted_text_2 = "@bbcmtd Wholesale Markets ablaze "

    assert remove_urls(org_text_2) == excepted_text_2

def test_remove_punc():
    input_text_1 = "Hello! How are you?"
    expected_output_1 = "Hello !  How are you ? "
    assert remove_punc(input_text_1), expected_output_1

def test_get_substitutions():
    # Define the dictionary for substitutions
    acronym_expected = {
        "MH370": "Malaysia Airlines Flight 370",
        "mÌ¼sica": "music",
        "okwx": "Oklahoma City Weather",
        "arwx": "Arkansas Weather",
        "gawx": "Georgia Weather",
        "scwx": "South Carolina Weather",
        "cawx": "California Weather",
        "tnwx": "Tennessee Weather",
        "azwx": "Arizona Weather",
        "alwx": "Alabama Weather",
        "wordpressdotcom": "wordpress",
        "usNWSgov": "United States National Weather Service",
        "Suruc": "Sanliurfa"
    }
    sub_file = os.path.join(cfg.TEXT_PROCESSING_MAP_PATH, "acronym.csv")
    assert os.path.exists(sub_file)

    substitutions = get_substitutions(sub_file)

    # Check if the substitutions match the expected substitutions
    assert substitutions == acronym_expected

# text subtitutions
def test_cleaning_text():
    org_text      = "arwx is bad so MH370 will be delayed"
    excepted_text = "Arkansas Weather is bad so Malaysia Airlines Flight 370 will be delayed" 

    sub_file = os.path.join(cfg.TEXT_PROCESSING_MAP_PATH, "acronym.csv")    
    assert cleaning_text(org_text, sub_file) == excepted_text

def test_processing_text():
    df = pd.DataFrame(
        {
            "id" : [1,2,3],
            "text": [
                "@bbcmtd Wholesale Markets ablaze http://t.co/lHYXEOHY6C",
                "#usNWSgov Special Weather Statement issued August 05 at 10:40PM EDT by NWS: ...STRONG THUNDERSTORM WILL IMPACT... http://t.co/TQ1rUQD4LG",
                "#Sismo DETECTADO #JapÌ_n 06:32:43 Miyagi Estimated seismic intensity 0 JST #??"
            ]
        }
    )
    
    excepted_df = pd.DataFrame(
        {
            "id" : [1,2,3],
            "text": [
               " @ bbcmtd Wholesale Markets ablaze ",
               " # United States National Weather Service Special Weather Statement issued August 05 at 10 : 40 PM EDT by NWS :   .  .  . STRONG THUNDERSTORM WILL IMPACT .  .  .  ",
               " # Sismo Detected  # Japan 06 : 32 : 43 Miyagi Estimated seismic intensity 0 JST  #  ?  ? "
            ]
        }
    ).reset_index()

    assert_frame_equal(processing_text(df, cfg.TEXT_PROCESSING_MAP_PATH).reset_index(), excepted_df)
