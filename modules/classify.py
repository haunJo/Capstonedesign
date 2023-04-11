import torch
from clip import clip
from PIL import Image

class Classifier():
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        
        self.labels = [
            "Standing",
            "Running",
            "Smoking",
            "Dumping",
            "Throwing",
            "Fighting"
        ]
        self.tokens = torch.cat([clip.tokenize(f"a photo of a person {c}") for c in self.labels]).to(self.device)

    def classify(self, source: Image.Image) -> str:
        image = source.resize((32, 32))
        image = self.preprocess(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image)
            text_features = self.model.encode_text(self.tokens)

        # Pick the top 5 most similar labels for the image
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        values, indices = similarity[0].topk(5)

        # Print the result of top 5 most similar labels
        # print("\nTop predictions:\n")
        # for value, index in zip(values, indices):
        #     print(f"{self.labels[index]:>16s}: {100 * value.item():.2f}%")
            
        # Return the most similar label
        return self.labels[indices[0]]