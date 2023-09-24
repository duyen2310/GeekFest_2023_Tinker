import dlib
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Example user database (for demonstration purposes)
# In a real application, you would use a proper database.
users = {
    'user1': {'password': 'password1', 'devices': [], 'face_data': None, 'temporary_feature': None},
    'user2': {'password': 'password2', 'devices': [], 'face_data': None, 'temporary_feature': None}
}

# Load face recognition model (pre-trained)
detector = dlib.get_frontal_face_detector()

# Function to compare faces
def compare_faces(face_data1, face_data2):
    # Implement your face comparison logic here
    # Return a similarity score (e.g., percentage match)
    # For simplicity, assume a static 80% match threshold
    return 80

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username in users and users[username]['password'] == password:
        device = request.json.get('device')
        
        if device not in users[username]['devices']:
            if users[username]['face_data'] is not None:
                new_face_data = request.json.get('face_data')
                similarity_score = compare_faces(users[username]['face_data'], new_face_data)
                if similarity_score >= 80:
                    users[username]['devices'].append(device)
                    return jsonify({'message': 'New device added successfully'}), 200
                else:
                    return jsonify({'message': 'Face recognition failed'}), 400
            else:
                return jsonify({'message': 'No face data available for comparison'}), 400
        else:
            return jsonify({'message': 'Login successful', 'new_device': False}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/temporary_use', methods=['POST'])
def temporary_use():
    username = request.json.get('username')
    selected_feature = request.json.get('selected_feature')

    if selected_feature not in users[username]['temporary_feature']:
        users[username]['temporary_feature'] = selected_feature
        # Generate temporary token and set expiration time (3 minutes)
        temporary_token = 'generated_token'  # Replace with actual token generation logic
        expiration_time = time.time() + (3 * 60)  # 3 minutes from now

        return jsonify({
            'message': 'Temporary token generated successfully',
            'temporary_token': temporary_token,
            'expiration_time': expiration_time
        }), 200
    else:
        return jsonify({'message': 'Selected feature already in use'}), 400

if __name__ == '__main__':
    app.run(debug=True)
