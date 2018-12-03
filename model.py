from parser import Parser
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

if __name__ == "__main__":
    parser = Parser()
    arr = parser.parse('process_log.txt', 'window_log.txt', 'file_log.txt')
    # split input data into train and validate
    train = arr[0:3700, :]
    validate = arr[3701:, :]

    parser_stranger = Parser()
    stranger_data = parser_stranger.parse('stranger_process_log.txt', 'stranger_window_log.txt', 'stranger_file_log.txt')

    parser_stranger2 = Parser()
    stranger_data2 = parser_stranger2.parse('stranger2_process_log.txt', 'stranger2_window_log.txt', 'stranger2_file_log.txt')
    
    gmm = GaussianMixture(n_components=15).fit(train)

    figure_train = plt.figure("train")
    plt.hist(gmm.score_samples(train), bins='auto')
    plt.title("train")
    figure_train.show()

    figure_validate = plt.figure("validate")
    plt.hist(gmm.score_samples(validate), bins='auto')
    plt.title("validate")
    figure_validate.show()

    figure_stranger = plt.figure("stranger")
    plt.hist(gmm.score_samples(stranger_data), bins='auto')
    plt.title("stranger")
    figure_stranger.show()

    figure_stranger = plt.figure("stranger2")
    plt.hist(gmm.score_samples(stranger_data2), bins='auto')
    plt.title("stranger")
    figure_stranger.show()

    raw_input()