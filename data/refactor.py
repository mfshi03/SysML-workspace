import json
import sys

def single_line(json_data):
    data = json.loads(json_data)
    single_line = json.dumps(data, separators=(',', ':'))
    return single_line

def reformat_json(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    with open(output_file, 'w') as f:
        for item in data:
            line = single_line(data)
            f.write(line.replace("\n",''))
            f.write('\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python reformat.py input_file.jsonl output_file.jsonl")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    #try:
    reformat_json(input_file, output_file)
    print(f"Reformatted JSON written to {output_file}")
    #except Exception as e:
        #print(f"Error: {e}")
        #sys.exit(1)