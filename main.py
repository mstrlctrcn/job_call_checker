from testing_grounds import get_725_calls_from_tumblr
from deliver_calls import send_message

def main():
	message = get_725_calls_from_tumblr()
	if message:
		send_message(message)
	else:
		send_message("There was an error. No call information available.")
if __name__ == "__main__":
	main()
