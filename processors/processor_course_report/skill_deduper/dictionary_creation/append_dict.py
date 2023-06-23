def main():
    import json
    from pathlib import Path

    path = Path(__file__).parent / "./initial_data"
    with open(f"{path}/skills_dict.json", 'r') as f:
        data = json.load(f)

    my_file = open(f"{path}/soft_skills.txt", "r")

    soft_skills = my_file.read()

    soft_skills_into_list = soft_skills.replace('\n', ' ').split(" ")

    for skill in soft_skills_into_list:
        data[skill.lower()] = [skill.lower()]

    ouput = json.dumps(data)

    with open(f"{path}/appended_dict.json", 'w') as fo:
        fo.write(ouput)


main()
