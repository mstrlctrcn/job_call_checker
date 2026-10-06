from urllib.request import Request, urlopen;
from urllib.error import HTTPError, URLError;
from bs4 import BeautifulSoup;
import re;
import html

def get_538_calls_from_website():
	# This needs work, but until I get some examples of how they input their job calls, I'm limited.
	# There are no calls currently. I will leave the posting in the notes. When there is a job call put in, I will post that to
	# the notes as well. In the meantime, this portion is on hold.
	req = Request('https://ibew725.tumblr.com/rss',
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Accept-Language': 'en-US,en;q=0.5'
			}
		)
	try:
		html = urlopen(req);
	except HTTPError as e:
		print(e);
	except URLError as e:
		print("The server could not be found.")
	else:
		html_text = html.read().decode('utf-8', errors='ignore')
		bs = BeautifulSoup(html_text, 'html.parser');
		posting = bs.find('div', id = "main-content");
		if posting:
			date = posting.find('title');
			calls = posting.find('description');
			listings = CallsListing((date).string, (calls).string);
			return listings.get_shortened_calls_new();
		else:
			print("Posting not found");

def get_725_calls_from_tumblr():
	req = Request('https://ibew725.tumblr.com/rss',
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5'
		}
	)
	try:
		html = urlopen(req);
	except HTTPError as e:
		print(e);
	except URLError as e:
		print("The server could not be found.")
	else:
		html_text = html.read().decode('utf-8', errors='ignore')
		bs = BeautifulSoup(html_text, 'xml');
		posting = bs.find('item');
		if posting:
			date = posting.find('title');
			calls = posting.find('description');
			listings = CallsListing((date).string, (calls).string);
			string1 = listings.get_shortened_calls_new()
			string2 = listings.get_calls_all();
			return string1 + "\n\n\n" + string2
		else:
			print("Posting not found");

class CallsListing():
	def __init__(self, date, text):
		text = html.unescape(text)
		self.full_text = text;
		self.date = date;
		self.calls = [];
		self.sections = re.findall(r"<p>(.+?)<\/p>", text);
		self.separate_calls();
	def separate_calls(self):
		for section in self.sections:
			if re.search(r"[Cc]all.?#", section):
				job = JobCall(section);
				self.calls.append(job);
	def get_shortened_calls_all(self):
		calls = []
		for call in self.calls:
			calls.append(call.oneline_str())
		return "\n".join(calls)
	def get_shortened_calls_new(self):
		calls = []
		for call in self.calls:
			if call.status.casefold() == "new".casefold():
				calls.append(call.oneline_str())
		return "\n".join(calls)
	def get_calls_all(self):
		calls = []
		for call in self.calls:
			calls.append(str(call))
		return "\n".join(calls)



class JobCall():
	def __init__(self, full_text):
		self.full_text = full_text;
		self.contractor = "";
		self.job_site = "";
		self.status = ""; #Is this a new or an open call?
		self.manpower = 0; #How many workers do they need?
		self.call_type = ""; #Short or Long?
		self.incentives = None; #If there are any listed.
		self.schedule = ""
		self.extract_content();
	def __str__(self):
		self_string = ""
		text = []
		text.append(f"Contractor: {self.contractor}");
		text.append(f"Job Site: {self.job_site}");
		text.append(f"Incentives: {self.incentives}")
		text.append(f"{self.call_type} call for {self.manpower}")
		text.append(f"This is a/an {self.status} call working {self.schedule}.")
		self_string = "\n".join(text);
		return self_string;
	def oneline_str(self):
		return(f"{self.schedule} at {self.job_site}. Incentives: {self.incentives}")
	def extract_content(self):
		self.contractor = re.search(r"- *(.+)needs", self.full_text).group(1);
		self.manpower = int(re.search(r"needs.*?(\d+).*?JW", self.full_text).group(1));
		self.call_type = re.search(r"a(.{4,7})?[Cc]all", self.full_text).group(1);
		self.job_site = re.search(r"at (.+?)\.", self.full_text).group(1);
		self.incentives = re.search(r"incentive.*?($.{4})", self.full_text)
		self.status = re.search(r"(.+?) [cC]all *#", self.full_text).group(1).strip();
		self.schedule = re.search(r"[wW]orking.*?(\d\/\d[^\.]*?)\.", self.full_text).group(1);
