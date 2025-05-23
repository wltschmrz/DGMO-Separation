# 모든 실행 진입점이라고 합시다.
from tqdm import tqdm
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import librosa.display as ld
import numpy as np
import librosa
import csv
import os

from utils import calculate_sisdr, calculate_sdr
from data_processing.audio_processing import read_wav_file

def plot_wav(wav_paths, save_path="./test/mel_compares/waveform_mel.png"):
    fig, axes = plt.subplots(2, len(wav_paths), figsize=(4 * len(wav_paths), 6))

    clip_duration = 10.24  # 클리핑 길이 (초)

    for i, wav_path in enumerate(wav_paths):
        sr, data = wav.read(wav_path)
        
        duration = len(data) / sr  # 오디오 길이(초)

        # Clip to first 5 seconds if longer
        if duration > clip_duration:
            data = data[: int(clip_duration * sr)]  # 앞 5초만 유지

        time = np.linspace(0, len(data) / sr, num=len(data))
        
        # Waveform
        axes[0, i].plot(time, data, lw=0.5)
        axes[0, i].set_title(f"Waveform {i+1}")
        axes[0, i].set_xlabel("Time (s)")
        axes[0, i].set_ylabel("Amplitude")

        # Mel Spectrogram
        y, sr = librosa.load(wav_path, sr=None)
        if len(y) > clip_duration * sr:  
            y = y[: int(clip_duration * sr)]
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        ld.specshow(mel_spec_db, sr=sr, x_axis="time", y_axis="mel", ax=axes[1, i])
        axes[1, i].set_title(f"Mel Spectrogram {i+1}")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_wav_mel(wav_arrays, sr=16000, save_path="./test/mel_compares/waveform_mel.png"):
    fig, axes = plt.subplots(2, len(wav_arrays), figsize=(4 * len(wav_arrays), 6))

    clip_duration = 10.24  # 클리핑 길이 (초)
    hop_length = 512       # Hop length 설정

    for i, wav in enumerate(wav_arrays):
        # NumPy 배열 확인 후 1D 변환
        if len(wav.shape) > 1:
            wav = wav.squeeze()

        # 샘플링 레이트 및 오디오 데이터 설정
        duration = len(wav) / sr  # 오디오 길이(초)

        # Clip to first 10.24 seconds if longer
        if duration > clip_duration:
            wav = wav[: int(clip_duration * sr)]  # 앞 10.24초만 유지

        time = np.linspace(0, len(wav) / sr, num=len(wav))

        # **Waveform 플로팅**
        axes[0, i].plot(time, wav, lw=0.5)
        axes[0, i].set_title(f"Waveform {i+1}")
        axes[0, i].set_xlabel("Time (s)")
        axes[0, i].set_ylabel("Amplitude")

        # **Mel Spectrogram 계산 및 플로팅**
        mel_spec = librosa.feature.melspectrogram(y=wav, sr=sr, n_mels=128, hop_length=hop_length)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

        # ✅ specshow()에 전달할 때 (n_mels, frames) 차원 확인
        ld.specshow(mel_spec_db, sr=sr, hop_length=hop_length, x_axis="time", y_axis="mel", ax=axes[1, i])

        axes[1, i].set_title(f"Mel Spectrogram {i+1}")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

wavs = [
    "./data/samples/A_cat_meowing.wav",
    "./test/result/cat.wav"
]

wav_src = read_wav_file(wavs[0], 10.24, 16000)
wav_sep = read_wav_file(wavs[1], 10.24, 16000)
sisdr = calculate_sisdr(ref=wav_src, est=wav_sep)
sdr = calculate_sdr(ref=wav_src, est=wav_sep)
print(sisdr, sdr)

wavnps = [wav_src, wav_sep]
plot_wav_mel(wavnps, save_path=f"./test/mel_compares/cat.png")



'''
audio_dir = 'data/vggsound'

with open(f'src/benchmarks/metadata/vggsound_eval.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    eval_list = [row for row in csv_reader][1:]

for eval_data in tqdm(eval_list[:50]):
    
    # idx, caption, _, _ = eval_data
    file_id, mix_wav, s0_wav, s0_text, s1_wav, s1_text = eval_data
    labels = s0_text
    idx = file_id
    # idx = file_id[-6:]

    mixture_path = os.path.join(audio_dir, mix_wav)
    source_path = os.path.join(audio_dir, s0_wav)
    # source_path = os.path.join(audio_dir, f'segment-{idx}.wav')
    # mixture_path = os.path.join(audio_dir, f'mixture-{idx}.wav')

    text = [labels][0]
    masked_path = f'./test/result/sep_{text}_{idx}_1.wav'
    # masked_path = f'./test/result/{text}_{idx}_1.wav'
    
    wavs = [
        mixture_path,
        source_path,
        masked_path,
        ]
    
    plot_wav_mel(wavs, save_path=f"./test/mel_compares/wav_mel_{idx}.png")
'''




# import argparse

# def inference(args):
#     # 모델 inference 코드
#     pass

# def evaluate(args):
#     # 모델 evaluation 코드
#     pass

# if __name__ == "__main__":

#     class LoadFromFile (argparse.Action):
#         def __call__ (self, parser, namespace, values, option_string = None):
#             with values as f:
#                 # parse arguments in the file and store them in the target namespace
#                 parser.parse_args(f.read().split(), namespace)


#     parser = argparse.ArgumentParser(description="Executing Diffusion-Guided Mask Optimization")

#     subparsers = parser.add_subparsers(dest="mode", required=True)

#     # Inference mode
#     infer_parser = subparsers.add_parser("infer", help="doing inference")
#     infer_parser.add_argument("--input_dir", type=str, required=True, help="mixed audio file directory")
#     infer_parser.add_argument("--output_dir", type=str, required=True, help="separated audio file directory")
#     infer_parser.add_argument("--model", type=str, required=True, help="choosing base model")
#     infer_parser.add_argument("--text", type=str, required=True, help="text caption to separate")
#     infer_parser.set_defaults(func=inference)

#     # Evaluation mode
#     eval_parser = subparsers.add_parser("eval", help="doing evaluation")
#     eval_parser.add_argument("--data_path", type=str, required=True, help="evaluation data path")
#     eval_parser.add_argument("--model", type=str, required=True, help="choosing base model")
#     eval_parser.set_defaults(func=evaluate)

#     args = parser.parse_args()
#     args.func(args)


