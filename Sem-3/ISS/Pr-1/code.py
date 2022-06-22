import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile
from scipy import signal
import copy
import math
import cmath


def center_clipping(in_list, value):
    out_list = copy.deepcopy(in_list)
    for frame in out_list:
        limit = np.abs(frame).max() * value
        for i in range(0, len(frame)):
            if np.abs(frame[i]) < limit:
                frame[i] = 0
            elif frame[i] > limit:
                frame[i] = 1
            else:
                frame[i] = -1
    return out_list


def auto_correlation(in_list):
    in_list = in_list.tolist()
    shift_list = copy.deepcopy(in_list)
    out_list = []
    for i in range(len(in_list)):
        if i != 0:
            in_list.append(0)
            shift_list.insert(0, 0)
        total = 0
        for j, k in zip(in_list, shift_list):
            total += j * k
        out_list.append(total)
    out_list = np.array(out_list)
    return out_list


def dft(in_list, size):
    in_list = in_list.tolist()
    out_list = []
    for i in range(size - len(in_list)):
        in_list.append(0)
    for k in range(size):
        total = 0
        for n in range(size):
            x = 2 * math.pi * n * k / size
            total += in_list[n] * (math.cos(x) - math.sin(x) * 1j)
        out_list.append(total)
    out_list = np.array(out_list)
    return out_list


def idft(in_list):
    in_list = in_list.tolist()
    size = len(in_list)
    out_list = []
    a = 2j * math.pi / size
    for n in range(size):
        total = 0
        for k in range(size):
            total += in_list[k] * cmath.exp(a * k * n)
        out_list.append(total / size)
    out_list = np.array(out_list)
    return out_list


def median_filtr(data, median_from):
    for i in range(len(data)):
        k = int((median_from - 1) / 2)
        if i < k:
            k = i
        if i >= (len(data) - k):
            k = len(data) - i - 1
        data[i] = np.median(data[i - k:i + k + 1])
    return data


# ################################ TASK 1 ################################ #

# importing tone wavs
fs_1, data_1 = wavfile.read('../audio/maskoff_tone.wav')
fs_2, data_2 = wavfile.read('../audio/maskon_tone.wav')

# ############################## END TASK 1 ############################## #


# ################################ TASK 2 ################################ #

# importing sentence wavs
fs_5, data_5 = wavfile.read('../audio/maskoff_sentence.wav')
fs_6, data_6 = wavfile.read('../audio/maskon_sentence.wav')
data_5 = data_5[:len(data_6)]

# ############################## END TASK 2 ############################## #


# ################################ TASK 3 ################################ #

# selecting one second long parts from the wavs (using cross-correlation)
data_start = 53360
sampling_freq = 16000
data_1 = data_1[data_start:data_start + sampling_freq]

coeff = 0
data2_start = 0
for i in range(0, data_2[:-data_1.size].size):
    n_coeff = np.corrcoef(data_1, data_2[i:i + data_1.size])[0, 1]
    if n_coeff > coeff:
        coeff = n_coeff
        data2_start = i

data_2 = data_2[data2_start:data2_start + data_1.size]

data_1_orig = copy.deepcopy(data_1)
data_2_orig = copy.deepcopy(data_2)
data_5_orig = copy.deepcopy(data_5)
data_6_orig = copy.deepcopy(data_6)

# doing the ustrednenie of signals
data_1 = data_1.copy()
data_2 = data_2.copy()
data_1 = data_1 - np.mean(data_1)
data_2 = data_2 - np.mean(data_2)

# normalization of signals into range [-1;1]
data_1 /= np.abs(data_1).max()
data_2 /= np.abs(data_2).max()

# splitting signals into frames
frame_size = int(0.02 * sampling_freq)
data_1 = [data_1[i:i + frame_size] for i in range(0, len(data_1), frame_size // 2)]
data_2 = [data_2[i:i + frame_size] for i in range(0, len(data_2), frame_size // 2)]
data_1.pop()
data_2.pop()

data_1_frames = copy.deepcopy(data_1)
data_2_frames = copy.deepcopy(data_2)

# plotting graph of one frame from both signals (tone wavs)
frame_no = 0
frame_1 = data_1[frame_no]
frame_2 = data_2[frame_no]
t = np.arange(data_1[frame_no].size) / fs_1
plt.figure()
plt.plot(t, frame_1, "-b")
plt.plot(t, frame_2, "-r")
plt.title('Rámec č. ' + str(frame_no))
plt.xlabel('t[s]')
plt.ylabel('y')
plt.legend(('bez rúška', 's rúškom'), loc='upper right')
plt.savefig('task_3.jpg')

# ############################## END TASK 3 ############################## #


# ################################ TASK 4 ################################ #

# using center clipping method
c_clip_val = 0.7
data_3 = center_clipping(data_1, c_clip_val)
data_4 = center_clipping(data_2, c_clip_val)

plt.figure(figsize=[6.4, 2.4])
plt.plot(t, frame_1, "-b")
plt.title('Rámec')
plt.xlabel('t[s]')
plt.ylabel('y')
plt.savefig('task_4a.jpg')

plt.figure(figsize=[6.4, 2.4])
plt.plot(t, data_3[frame_no], "-b")
plt.title('Centrálne klipovanie so ' + str(c_clip_val * 100) + ' %')
plt.xlabel('t[s]')
plt.ylabel('y')
plt.savefig('task_4b.jpg')

# using autocorrelation on the clipped signals
data_3 = [np.correlate(frame, frame, mode="full")[len(frame) - 1:] for frame in data_3]
data_4 = [np.correlate(frame, frame, mode="full")[len(frame) - 1:] for frame in data_4]

threshold_freq = 500
threshold = int(fs_1 / threshold_freq)

plt.figure(figsize=[6.4, 2.4])
plt.plot(t * fs_1, data_3[frame_no], "-b")
plt.title('Autokorelácia')
plt.xlabel('vzorky')
plt.ylabel('y')
plt.axvline(threshold, color="black", label="Prah")
plt.stem([threshold + np.argmax(data_3[frame_no][threshold:])], [np.max(data_3[frame_no][threshold:])], linefmt='red', markerfmt="bo", label="Lag")
plt.legend()
plt.savefig('task_4c.jpg')

# calculating fundamental frequencies for each frame
data_3 = [fs_1 / (threshold + np.argmax(frame[threshold:])) for frame in data_3]
data_4 = [fs_2 / (threshold + np.argmax(frame[threshold:])) for frame in data_4]

# plotting graph that compares fundamental frequencies of tone signals
plt.figure(figsize=[6.4, 2.4])
t = np.arange(len(data_1))
plt.plot(t, data_3, "-b")
plt.plot(t, data_4, "-r")
plt.title('Základné frekvencie rámcov')
plt.xlabel('rámce')
plt.ylabel('f0')
plt.legend(('bez rúška', 's rúškom'), loc='lower right')
plt.savefig('task_4d.jpg')

# calculating expected values and variances of fundamental frequencies of tone signals
expected_value_1 = np.mean(data_3)
expected_value_2 = np.mean(data_4)

variance_1 = np.var(data_3)
variance_2 = np.var(data_4)

# print(expected_value_1, expected_value_2, variance_1, variance_2)

fund_freq_1 = copy.deepcopy(data_3)
fund_freq_2 = copy.deepcopy(data_4)

# ############################## END TASK 4 ############################## #


# ################################ TASK 5 ################################ #

# applying Fourier transform on signals from task 3
size = 1024
data_1 = [np.fft.fft(frame, n=size) for frame in data_1]
data_2 = [np.fft.fft(frame, n=size) for frame in data_2]

# selecting non-overlapping parts of frames (first half of each)
data_3 = [frame[:int(size/2)] for frame in data_1]
data_4 = [frame[:int(size/2)] for frame in data_2]

# applying given logarithm formula
data_3 = [[10 * math.log(np.abs(i)**2, 10) for i in frame] for frame in data_3]
data_4 = [[10 * math.log(np.abs(i)**2, 10) for i in frame] for frame in data_4]

# plotting spectograms
plt.figure()
plt.title('Spektogram bez rúška')
plt.xlabel('t[s]')
plt.ylabel('frekvencia')
plt.imshow(np.array(data_3).T, extent=(0, 1, 0, 8000), aspect="auto", origin='lower')
plt.colorbar()
plt.savefig('task_5a.jpg')

plt.figure()
plt.title('Spektogram s rúškom')
plt.xlabel('t[s]')
plt.ylabel('frekvencia')
plt.imshow(np.array(data_4).T, extent=(0, 1, 0, 8000), aspect="auto", origin='lower')
plt.colorbar()
plt.savefig('task_5b.jpg')

# ############################## END TASK 5 ############################## #


# ################################ TASK 6 ################################ #

# calculating frequency response of the mask
freq_response = [y / x for x, y in zip(data_1, data_2)]
freq_response = [np.mean(np.abs(i)) for i in np.array(freq_response).T]
freq_response = freq_response[:int(size/2)]
freq_resp_to_plot = [10 * math.log(np.abs(i)**2, 10) for i in freq_response]

# plotting frequency response
plt.figure()
t = np.arange(size / 2)
plt.plot(t, freq_resp_to_plot, "-b")
plt.title('Frekvenčná charakteristika rúška')
plt.xlabel('frekvencia')
plt.ylabel('y')
plt.savefig('task_6.jpg')

# ############################## END TASK 6 ############################## #


# ################################ TASK 7 ################################ #

# calculating impulse response
impulse_response = np.fft.ifft(np.array(freq_response), n=size)
impulse_response = impulse_response[:int(size/2)]

# plotting impulse response
plt.figure()
plt.plot(t, impulse_response.real, "-b")
plt.title('Impulzná odozva')
plt.xlabel('frekvencia')
plt.ylabel('y')
plt.savefig('task_7.jpg')

# ############################## END TASK 7 ############################## #


# ################################ TASK 8 ################################ #

# simulating function of the mask
sim_mask_sentence = signal.lfilter(impulse_response.real, [1], data_5)
sim_mask_tone = signal.lfilter(impulse_response.real, [1], data_1_orig)

# casting signals to int16 and writing them to files
sim_mask_sentence = sim_mask_sentence.astype(np.int16)
sim_mask_tone = sim_mask_tone.astype(np.int16)

wavfile.write('../audio/sim_maskon_sentence.wav', fs_5, sim_mask_sentence)
wavfile.write('../audio/sim_maskon_tone.wav', fs_5, sim_mask_tone)

data_2 = data_2_orig - np.mean(data_2_orig)
data_2 /= np.abs(data_2).max()
data_6 = data_6 - np.mean(data_6)
data_6 /= np.abs(data_6).max()
sim_mask_tone = sim_mask_tone - np.mean(sim_mask_tone)
sim_mask_tone /= np.abs(sim_mask_tone).max()
sim_mask_sentence = sim_mask_sentence - np.mean(sim_mask_sentence)
sim_mask_sentence /= np.abs(sim_mask_sentence).max()

# plotting graphs comparing the simulated mask with the real one
plt.figure()
t = np.arange(np.size(data_1_orig)) / sampling_freq
plt.plot(t, data_2, "-r")
plt.plot(t, sim_mask_tone, "-b")
plt.title('Porovnanie tónu s reálnym a so simulovaným rúškom')
plt.xlabel('t[s]')
plt.ylabel('y')
plt.legend(('reálne rúško', 'simulované rúško'), loc='upper right')
plt.savefig('task_8a.jpg')

plt.figure()
t = np.arange(np.size(data_6)) / sampling_freq
plt.plot(t, data_6, "-r")
plt.plot(t, sim_mask_sentence, "-b")
plt.title('Porovnanie vety s reálnym a so simulovaným rúškom')
plt.xlabel('t[s]')
plt.ylabel('y')
plt.legend(('reálne rúško', 'simulované rúško'), loc='upper right')
plt.savefig('task_8b.jpg')

# ############################## END TASK 8 ############################## #


# ############################### TASK B12 ############################### #

# doing center clipping with value set as 0.9
frame_no = 16
c_clip_val = 0.9
data_3 = center_clipping(data_1_frames, c_clip_val)
data_4 = center_clipping(data_2_frames, c_clip_val)
data_3 = [np.correlate(frame, frame, mode="full")[len(frame) - 1:] for frame in data_3]
data_4 = [np.correlate(frame, frame, mode="full")[len(frame) - 1:] for frame in data_4]
threshold_freq = 500
threshold = int(fs_1 / threshold_freq)

plt.figure(figsize=[6.4, 2.4])
t = np.arange(data_4[frame_no].size)
plt.plot(t, data_4[frame_no], "-b")
plt.title('Autokorelácia rámca, kde nastala zmena')
plt.xlabel('vzorky')
plt.ylabel('y')
plt.axvline(threshold, color="black", label="Prah")
plt.stem([threshold + np.argmax(data_4[frame_no][threshold:])], [np.max(data_4[frame_no][threshold:])], linefmt='red', markerfmt="bo", label="Lag")
plt.legend()
plt.savefig('task_12a.jpg')

data_3 = [fs_1 / (threshold + np.argmax(frame[threshold:])) for frame in data_3]
data_4 = [fs_2 / (threshold + np.argmax(frame[threshold:])) for frame in data_4]

# plotting graph that compares fundamental frequencies of tone signals without using the median filtration
plt.figure(figsize=[6.4, 2.4])
t = np.arange(len(data_3))
plt.plot(t, data_3, "-b")
plt.plot(t, data_4, "-r")
plt.title('Základné frekvencie rámcov bez použitia mediánovej filtrácie')
plt.xlabel('rámce')
plt.ylabel('f0')
plt.legend(('bez rúška', 's rúškom'), loc='lower right')
plt.savefig('task_12b.jpg')

k = 3  # median of k elements
data_3 = median_filtr(data_3, k)
data_4 = median_filtr(data_4, k)

# plotting graph that compares fundamental frequencies of tone signals with the use of the median filtration
plt.figure(figsize=[6.4, 2.4])
plt.plot(t, data_3, "-b")
plt.plot(t, data_4, "-r")
plt.title('Základné frekvencie rámcov s použitím mediánovej filtrácie')
plt.xlabel('rámce')
plt.ylabel('f0')
plt.legend(('bez rúška', 's rúškom'), loc='lower right')
plt.savefig('task_12c.jpg')

# ############################# END TASK B12 ############################# #


# ############################### TASK B13 ############################### #

# deleting all frames with different fundamental frequencies
data_1 = [data_1_frames[i] for i in range(len(data_1_frames)) if fund_freq_1[i] == fund_freq_2[i]]
data_2 = [data_2_frames[i] for i in range(len(data_2_frames)) if fund_freq_1[i] == fund_freq_2[i]]

# calculating frequency response
size = 1024
data_1 = [np.fft.fft(frame, n=size) for frame in data_1]
data_2 = [np.fft.fft(frame, n=size) for frame in data_2]
freq_response = [y / x for x, y in zip(data_1, data_2)]
freq_response = [np.mean(np.abs(i)) for i in np.array(freq_response).T]
freq_response = freq_response[:int(size/2)]
freq_resp_to_plot_2 = [10 * math.log(np.abs(i)**2, 10) for i in freq_response]

# plotting comparison of frequency responses
plt.figure()
t = np.arange(size / 2)
plt.plot(t, freq_resp_to_plot, "-b")
plt.plot(t, freq_resp_to_plot_2, "-r")
plt.title('Frekvenčná charakteristika rúška')
plt.xlabel('frekvencia')
plt.ylabel('y')
plt.legend(('zo všetkých rámcov', 'z rámcov s rovnakou f0 '), loc='upper right')
plt.savefig('task_13.jpg')

impulse_response = np.fft.ifft(np.array(freq_response), n=size)[:int(size/2)]

sim_mask_sentence = signal.lfilter(impulse_response.real, [1], data_5)
sim_mask_tone = signal.lfilter(impulse_response.real, [1], data_1_orig)

wavfile.write('../audio/sim_maskon_sentence_only_match.wav', fs_5, sim_mask_sentence.astype(np.int16))
wavfile.write('../audio/sim_maskon_tone_only_match.wav', fs_5, sim_mask_tone.astype(np.int16))


# ############################# END TASK B13 ############################# #


# ############################### TASK B15 ############################### #

# splitting signals into frames
frame_size_unique = int(sampling_freq / 100)
frame_size = int(0.025 * sampling_freq)
data_1 = [data_1_orig[i:i + frame_size] for i in range(0, len(data_1_orig), frame_size_unique)]
data_2 = [data_2_orig[i:i + frame_size] for i in range(0, len(data_2_orig), frame_size_unique)]
data_1.pop()
data_1.pop()
data_2.pop()
data_2.pop()

frame_size = int(0.02 * sampling_freq)
data_3 = [data_5_orig[i:i + frame_size] for i in range(0, len(data_5_orig), frame_size_unique)]
data_3.pop()

# clipping tone signals
c_clip_val = 0.7
data_1_cc = center_clipping(data_1, c_clip_val)
data_2_cc = center_clipping(data_2, c_clip_val)

# calculating left and right phase difference
l_phase_diff = [np.argmax(np.correlate(frame_1, frame_2, mode="full")[len(frame_1) - 1:]) for frame_1, frame_2 in zip(data_1_cc, data_2_cc)]
r_phase_diff = [np.argmax(np.correlate(frame_2, frame_1, mode="full")[len(frame_1) - 1:]) for frame_1, frame_2 in zip(data_1_cc, data_2_cc)]

# searching for the smaller phase difference for each frame and then moving the signals accordingly
for i in range(len(l_phase_diff)):
    minimum = min(l_phase_diff[i], r_phase_diff[i])
    if minimum == 0:
        continue
    elif l_phase_diff[i] <= r_phase_diff[i]:
        data_1[i] = data_1[i][minimum:]
        data_2[i] = data_2[i][:-minimum]
    else:
        data_1[i] = data_1[i][:-minimum]
        data_2[i] = data_2[i][minimum:]

# trimming the frames to a constant size of 0.02 s
data_1 = [frame[:frame_size] for frame in data_1]
data_2 = [frame[:frame_size] for frame in data_2]

# plotting graphs
plt.figure()
t = np.arange(frame_size) / fs_1
frame_no = 61
plt.plot(t, data_1_orig[int(frame_no * frame_size / 2):int((frame_no / 2 + 1) * frame_size)], "-b")
plt.plot(t, data_2_orig[int(frame_no * frame_size / 2):int((frame_no / 2 + 1) * frame_size)], "-r")
plt.title('Rámec pred zarovnávaním')
plt.xlabel('t[s]')
plt.ylabel('y')
plt.legend(('bez rúška', 's rúškom'), loc='upper right')
plt.savefig('task_15a.jpg')

plt.figure()
plt.plot(t, data_1[frame_no], "-b")
plt.plot(t, data_2[frame_no], "-r")
plt.title('Rámec po zarovnávaní')
plt.xlabel('t[s]')
plt.ylabel('y')
plt.legend(('bez rúška', 's rúškom'), loc='upper right')
plt.savefig('task_15b.jpg')

plt.figure()
t = np.arange(len(l_phase_diff))
plt.plot(t, [min(i, j) for i, j in zip(l_phase_diff, r_phase_diff)], "-b")
plt.title('Priebeh fázového posunu')
plt.xlabel('rámce')
plt.ylabel('vzorky')
plt.savefig('task_15c.jpg')

# calculating the filter (mask)
data_1 = [np.fft.fft(frame, n=size) for frame in data_1]
data_2 = [np.fft.fft(frame, n=size) for frame in data_2]
freq_response = [y / x for x, y in zip(data_1, data_2)]
freq_response = [np.mean(np.abs(i)) for i in np.array(freq_response).T]
freq_response = freq_response[:int(size/2)]
impulse_response = np.fft.ifft(np.array(freq_response), n=size)[:int(size/2)]

# simulating the filter and saving output
sim_mask_tone = signal.lfilter(impulse_response.real, [1], data_1_orig)
sim_mask_sentence = signal.lfilter(impulse_response.real, [1], data_5_orig)

wavfile.write('../audio/sim_maskon_sentence_phase.wav', fs_1, sim_mask_sentence.astype(np.int16))
wavfile.write('../audio/sim_maskon_tone_phase.wav', fs_1, sim_mask_tone.astype(np.int16))

# ############################# END TASK B15 ############################# #
