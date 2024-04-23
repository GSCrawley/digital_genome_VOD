# # Cognitive Network Manager main
# from flask import Flask, request, jsonify
# import requests
# app = Flask(__name__)
# @app.route('/')
# def ():
# 	data = request.json
# 	number = data['number’]
# 	response = requests.post('http://127.0.0.1:5002/multiply', json={'number': number})
# 	if response.status_code == 200:
# 		result = response.json()['result’]
# 		print(result)
# 		return jsonify({'result': result})
# 	else:
# 		return jsonify({'error': 'Failed to process the number.'})
# @app.route('/add', methods=['POST'])
# def add():
# 	data = request.json
# 	number = data['number’]
# 	response = requests.post('http://127.0.0.1:5003/add', json={'number': number})
# 	if response.status_code == 200:
# 		result = response.json()['result’]
# 		print(result)
# 		return jsonify({'result': result})
# 	else:
# 		return jsonify({'error': 'Failed to process the number.'})
# if __name__ == '__main__’:
# 	app.run(debug=True, port=5001)

