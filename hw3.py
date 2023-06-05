from flask import Flask, render_template, request, send_file,Response
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
seq=[]
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        sequences = []
        sequences = request.form['sequences'].splitlines()
        format='png'
        image_data = generate_sequence_logo(sequences,format)
        pas(sequences)
        return render_template('index.html', image_data=image_data,sequences=sequences)
    return render_template('index.html')
def pas(sequences):
    global seq
    seq = sequences
    return seq
def generate_sequence_logo(sequences,format):
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
    if format == 'svg':
        plt.savefig(buffer, format='svg')
    elif format == 'jpg':
        plt.savefig(buffer, format='jpg')
    else:
        plt.savefig(buffer, format='png')
    
    buffer.seek(0)

    plt.savefig('sequence.jpg')
    plt.savefig('sequence.png')
    plt.savefig('sequence.svg')
    plt.close()

    # Clear the figure to release memory
    plt.close(fig)

    image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_data

@app.route('/download', methods=['GET'])
def download():
    format = request.args.get('format', 'png')
    if format == 'svg':
        mimetype = 'image/svg+xml'
        extension = 'svg'
        attachment_filename='sequence_logo.' + extension
        image_data = generate_sequence_logo(seq,extension)  # Generate SVG image data
        image_data = base64.b64decode(image_data)
    elif format == 'jpg':
        mimetype = 'image/jpeg'
        extension = 'jpg'
        attachment_filename='sequence_logo.' + extension
        image_data = generate_sequence_logo(seq,extension)  # Generate JPG image data
        image_data = base64.b64decode(image_data)
    else:
        mimetype = 'image/png'
        extension = 'png'
        attachment_filename='sequence_logo.' + extension
        image_data = generate_sequence_logo(seq,extension)  # Generate PNG image data
        image_data = base64.b64decode(image_data)

    #return send_file(attachment_filename, as_attachment=True)
    #return send_file(BytesIO(image_data), attachment_filename='sequence_logo.' + extension, as_attachment=True, mimetype=mimetype)
    return send_file(BytesIO(image_data), mimetype=mimetype, as_attachment=True, download_name='sequence_logo.' + extension)

if __name__ == '__main__':
    app.run(debug=True)
