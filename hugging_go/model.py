from transformers.trainer_utils import get_last_checkpoint
from transformers import Trainer, TrainingArguments
from transformers import DistilBertConfig, DistilBertForSequenceClassification
from transformers import AutoModelForSequenceClassification, AutoTokenizer

_MODEL_PATH = 'model/'

def _bert_config(features):
    id2label = {idx: features['label'].int2str(idx) for idx in range(362)}
    label2id = {value: key for key, value in id2label.items()}

    config = DistilBertConfig(
        vocab_size=362 + 5,
        num_labels=362,
        id2label=id2label,
        label2id=label2id,

        # values inspired by TinyBert-4L (https://huggingface.co/huawei-noah/TinyBERT_General_4L_312D/blob/main/config.json)
        n_layers=4,
        hidden_dim=1200,
        dim=312
    )
    return config

def _bert_model(features):
    return DistilBertForSequenceClassification(_bert_config(features))

def pretrained_model():
    latest_checkpoint = get_last_checkpoint(_MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(latest_checkpoint)
    tokenizer = AutoTokenizer.from_pretrained(latest_checkpoint)

    def _pipeline(text):
        tokens = tokenizer(text, return_tensors='pt')
        result = model.forward(
            input_ids=tokens['input_ids'],
            attention_mask=tokens['attention_mask']
        )
        logits = result.logits[0, :].softmax(-1).detach().numpy()
        id2label = model.config.id2label

        return [[
            {
                'label': id2label[i],
                'score': logits[i]
            }
            for i in id2label.keys()
        ]]

    return _pipeline

def train(dataset, *, tokenizer):
    dataset = dataset.shuffle()
    features = dataset['train'].features

    trainer = Trainer(
        model=_bert_model(features),
        args=TrainingArguments(
            output_dir=_MODEL_PATH,
            overwrite_output_dir=True,
            per_device_train_batch_size=32,
            fp16=True,
        ),
        train_dataset=dataset['train'],
        tokenizer=tokenizer
    )
    trainer.train()
