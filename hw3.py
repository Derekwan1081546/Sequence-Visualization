from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)
seq=[]
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        sequences = []
        sequences = request.form['sequences'].splitlines()
        image_data = generate_sequence_logo(sequences)
        pas(sequences)
        return render_template('index.html', image_data=image_data,sequences=sequences)
    return render_template('index.html')
def pas(sequences):
    global seq
    seq = sequences
    return seq
def generate_sequence_logo(sequences):
    if not sequences:
        raise ValueError("No sequences provided")

    seq_length = len(sequences[0])
    for sequence in sequences:
        if len(sequence) != seq_length:
            raise ValueError("All sequences must have the same length")

    max_length = 16  # Maximum sequence length

    # Truncate or pad sequences to the maximum length
    sequences = [seq[:max_length].ljust(max_length, '-') for seq in sequences]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Assign colors to amino acids
    colors = {
        'A': '#99CC00', 'R': '#0000FF', 'N': '#FFCC00', 'D': '#FF0000',
        'C': '#FFFF00', 'Q': '#00FF00', 'E': '#FF3300', 'G': '#FF66CC',
        'H': '#0066FF', 'I': '#009999', 'L': '#00FFCC', 'K': '#6600FF',
        'M': '#00CC00', 'F': '#3300FF', 'P': '#FF00FF', 'S': '#FF6633',
        'T': '#FF9900', 'W': '#9933FF', 'Y': '#FF3366', 'V': '#00CCFF'
    }

    seq_length = len(sequences[0])
    num_sequences = len(sequences)

    for i in range(max_length):
        counts = {}
        for sequence in sequences:
            if i < len(sequence) and sequence[i] != '-':
                amino_acid = sequence[i]
                if amino_acid != '\r' and amino_acid != '\n':
                    if amino_acid in counts:
                        counts[amino_acid] += 1
                    else:
                        counts[amino_acid] = 1

        total_count = sum(counts.values())

        for amino_acid, count in counts.items():
            ax.bar(i, count / total_count, color=colors[amino_acid], width=1)

    ax.set_xlim(-0.5, seq_length - 0.5)
    ax.set_ylim(0, 1)
    ax.set_xticks(range(seq_length))
    ax.set_xticklabels(range(1, seq_length+1))
    ax.set_xlabel('Position')
    ax.set_ylabel('Relative Frequency')

    plt.tight_layout()

    # Save the figure to a buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    plt.savefig('sequence.jpg')
    plt.savefig('sequence.png')
    plt.savefig('sequence.svg')
    plt.close()

    # Clear the figure to release memory
    plt.close(fig)
    return buffer.getvalue()

@app.route('/download', methods=['GET'])
def download():
    format = request.args.get('format', 'png')
    if format == 'svg':
        mimetype = 'image/svg+xml'
        extension = 'svg'
        image_data = generate_sequence_logo_svg(seq)  # Generate SVG image data
    elif format == 'jpg':
        mimetype = 'image/jpeg'
        extension = 'jpg'
        image_data = generate_sequence_logo_jpg(seq)  # Generate JPG image data
    else:
        mimetype = 'image/png'
        extension = 'png'
        image_data = generate_sequence_logo_png(seq)  # Generate PNG image data

    return send_file(BytesIO(image_data), attachment_filename='sequence_logo.' + extension, as_attachment=True, mimetype=mimetype)

def generate_sequence_logo_svg(sequences):
    # Generate the sequence logo using matplotlib
    fig, ax = generate_sequence_logo(sequences)

    # Save the figure to a buffer as SVG
    buffer = BytesIO()
    fig.savefig(buffer, format='svg')
    buffer.seek(0)

    # Clear the figure to release memory
    plt.close(fig)

    # Return the SVG image data
    return buffer.getvalue()

def generate_sequence_logo_jpg(sequences):
    # Generate the sequence logo using matplotlib
    fig, ax = generate_sequence_logo(sequences)

    # Save the figure to a buffer as JPG
    buffer = BytesIO()
    fig.savefig(buffer, format='jpg')
    buffer.seek(0)

    # Clear the figure to release memory
    plt.close(fig)

    # Return the JPG image data
    return buffer.getvalue()

def generate_sequence_logo_png(sequences):
    # Generate the sequence logo using matplotlib
    fig, ax = generate_sequence_logo(sequences)

    # Save the figure to a buffer as PNG
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    # Clear the figure to release memory
    plt.close(fig)

    # Return the PNG image data
    return buffer.getvalue()

if __name__ == '__main__':
    app.run(debug=True)
