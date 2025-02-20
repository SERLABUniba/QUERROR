from openai import OpenAI
import os
import json

from openai import OpenAI
client = OpenAI(api_key="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")

text = ("RUN conda update -n base conda && /\ git clone --depth 1 https://github.com/deepchem/deepchem.git && \ cd "
        "deepchem && \ - source scripts/light/install_deepchem.sh 3.8 cpu tensorflow && \ + "
        "source scripts/light/install_deepchem.sh 3.10 cpu tensorflow && \ conda activate deepchem && \ pip install "
        "-e . && \ conda clean -afy && /")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a security expert, who can analyse code changes."},
    {"role": "user", "content": f"What bugs does this code change resolve? "
                                f"Does this solve any vulnerabilities? "
                                f"Is the fix related to quantum computing or not? : {text}"}
  ]
)

"""for chunk in completion:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")"""

print(completion.choices[0].message)

"""client = OpenAI(api_key="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")

# Define the prompt for text generation
prompt_text = "Once upon a time,"

completion = client.completions.create(
    model='gpt-3.5-turbo',
    prompt=prompt_text,
    max_tokens=100
)

generated_text = completion.choices[0].text.strip()
print("Generated Text:")
print(generated_text)
"""
"""completion = client.completions.create(model='text-davinci-002', prompt=prompt_text)
print(completion.choices[0].text)
print(dict(completion).get('usage'))
print(completion.model_dump_json(indent=2))
"""
# Generate text using OpenAI's GPT-3 model
"""response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt_text,
    temperature=0.7,
    max_tokens=100
)"""

# Get the generated text from the response
"""generated_text = response.choices[0].text.strip()

# Print the generated text
print("Generated Text:")
print(generated_text)"""
