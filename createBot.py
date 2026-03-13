# Standard library imports
import os
import shutil

def prompt(msg, hint=None):
	if hint:
		print(f"{msg} ({hint})")
	else:
		print(msg)
	return input(": ").strip()

def main():
	# 1. Ask for mobile number
	mobile = prompt("Enter your Telegram phone number", "Format: +91XXXXXXXXXX")
	if not mobile.startswith('+91') or len(mobile) < 12:
		print("Invalid mobile number format. Please use +91XXXXXXXXXX.")
		return
	# 2. Ask for api_id
	api_id = prompt("Enter your Telegram api_id", "Find it at https://my.telegram.org/apps")
	# 3. Ask for api_hash
	api_hash = prompt("Enter your Telegram api_hash")

	# 4. Create new account folder
	last4 = mobile[-4:]
	new_folder = f"account6_{last4}"
	src_folder = "account6_4139_Ban"
	dst_path = os.path.join(os.getcwd(), new_folder)
	src_path = os.path.join(os.getcwd(), src_folder)
	if not os.path.exists(src_path):
		print(f"Source folder '{src_folder}' not found.")
		return
	if os.path.exists(dst_path):
		print(f"Target folder '{new_folder}' already exists.")
		return
	shutil.copytree(src_path, dst_path)
	print(f"Copied '{src_folder}' to '{new_folder}'.")

	# 5. Update api.py in new folder
	api_py = os.path.join(dst_path, "api.py")
	api_py_content = f"Mobile = '{mobile}'\napi_id = {api_id}\napi_hash = '{api_hash}'\nsession_name = 'auto_send_session'\n\ndef apiId():\n    return api_id\n\ndef apiHash():\n    return api_hash\n\ndef sessionName():\n    return session_name\n"
	with open(api_py, "w", encoding="utf-8") as f:
		f.write(api_py_content)
	print(f"Updated api.py in '{new_folder}'.")

	# 6. Show instructions
	print("\n--- Next Steps ---")
	print(f"To run each bot, open a terminal and execute:")
	for i in range(1, 11):
		print(f"python {new_folder}/bot{i}/start.py")
	print("\nRun each bot one by one. Your new Telegram account is ready for autoSendBot.")

if __name__ == "__main__":
	main()
