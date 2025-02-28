from multiprocessing import Process, Manager, cpu_count
from collections import defaultdict

def process(data, results):
    for t in data:
        if t not in results:
            results[t] = 0
        results[t] += 1

def main():
    ## 텍스트 파일 읽기 및 가공
    example_text = open("./example.txt", "r").read()
    example_text = [i.lower().replace("'s","").replace(",","").replace(".","").replace("?","")
                    for i in example_text.replace("\n", " ").split(" ") if i != '']
    n = len(example_text)

    ## 단어가 얼마나 나오는지 저장할 공유 dictionary
    results = Manager().dict()

    ## multi process를 사용하여 단어 수를 세기위함
    ## 현재 실행되고 있는 CPU Core 수만큼 Process를 만듦
    step = n // cpu_count()
    processes = list()
    for i in range(0, n, step):
        p = Process(target=process, args=(example_text[i:i+step], results))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    resutls = dict(results)

    ## 결과 도출하는 과정
    print(f"1. Rebecca : {results['rebecca']}")

    sorted_results = sorted(results.items(), key = lambda item: item[1],reverse=True)
    
    top5_words = list()
    for word, _ in sorted_results:
        if len(word) >= 4:
            top5_words.append(word)
        if len(top5_words) == 5:
            break
    
    print(f"2. Top5 Words: {', '.join(top5_words)}")

if __name__ == "__main__":
    main()