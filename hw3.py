from flask import Flask, render_template, request
from matplotlib import pyplot as plt
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sequences = request.form['sequences'].split('\n')
        generate_logo(sequences)
    return render_template('index.html')

def generate_logo(sequences):
    # Implement sequence logo generation logic here
    # Use the Matplotlib and NumPy libraries to create the logo
    # Save the output as JPG, PNG, and SVG files
    
    # Example code to plot a simple logo
    plt.figure(figsize=(8, 4))
    logo_data = np.random.rand(len(sequences), len(sequences[0]))
    plt.imshow(logo_data, cmap='hot', aspect='auto')
    plt.axis('off')
    plt.savefig('logo.png')
    plt.savefig('logo.svg')
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)