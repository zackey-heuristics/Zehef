"""
This module is used to output the Zehef result (only account search) in JSON format.

Usage:
    python only_account_search_json_output.py [EMAIL] [--output OUTPUT_JSON_FILE_PATH]

Options:
    EMAIL: str
        Email address to search for.
    OUTPUT_JSON_FILE_PATH: pathlib.Path
        Output JSON file path.
"""
import argparse
import asyncio
import datetime
import json
import pathlib
import sys

from email_validator import validate_email, EmailNotValidError

from modules import *


async def maincore():
    parser = argparse.ArgumentParser(
        description="Output the Zehef result (only account search) in JSON format."
    )
    parser.add_argument(
        "email",
        type=str,
        help="Search account information on email."
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        help="Output JSON file path."
    )
    args = parser.parse_args()
    output_json_file_path = args.output
    
    try:
        validator = validate_email(args.email)
        target_email = validator.email
    except EmailNotValidError as e:
        print("Invalid email address.", file=sys.stderr)
        sys.exit(1)
    
    pastebin_results = await PastebinDumper4JSON(target_email).paste_check()
    cavalier_results = await Cavalier4JSON(target_email).loader()
    
    adobe_result = await adobe4json(target_email)
    bandlab_result = await bandlab4json(target_email)
    chess_result = await chess4json(target_email)
    deezer_result = deezer4json(target_email)
    duolingo_result = await duolingo4json(target_email)
    flickr_result = await flickr4json(target_email)
    github_result = await github4json(target_email)
    gravatar_result = await gravatar4json(target_email)
    imgur_result = imgur4json(target_email)
    instagram_result = await instagram4json(target_email)
    picsart_result = await picsart4json(target_email)
    pinterest_result = await pinterest4json(target_email)
    protonmail_result = await protonmail4json(target_email)
    pornhub_result = pornhub4json(target_email)
    spotify_result = await spotify4json(target_email)
    strava_result = await strava4json(target_email)
    x_result = await x4json(target_email)
    
    account_search_results = {
        "email": target_email,
        "searched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "pastebin": pastebin_results,
        "cavalier": cavalier_results,
        "adobe": adobe_result,
        "bandlab": bandlab_result,
        "chess": chess_result,
        "deezer": deezer_result,
        "duolingo": duolingo_result,
        "flickr": flickr_result,
        "github": github_result,
        "gravatar": gravatar_result,
        "imgur": imgur_result,
        "instagram": instagram_result,
        "picsart": picsart_result,
        "pinterest": pinterest_result,
        "protonmail": protonmail_result,
        "pornhub": pornhub_result,
        "spotify": spotify_result,
        "strava": strava_result,
        "x": x_result
    }
    
    if output_json_file_path:
        with open(output_json_file_path, "w") as f:
            json.dump(account_search_results, f, indent=4, ensure_ascii=False)
        print(f"{pathlib.Path(output_json_file_path).resolve()}")
    else:
        print(json.dumps(account_search_results, indent=4, ensure_ascii=False))
        

def main():
    asyncio.run(maincore())


if __name__ == "__main__":
    main()
