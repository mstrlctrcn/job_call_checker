from urllib.request import Request, urlopen;
from urllib.error import HTTPError, URLError;
from bs4 import BeautifulSoup;
import re;

def get_725_calls_from_tumblr():
	req = Request('https://ibew725.tumblr.com/', headers={f'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64'})
	try:
		html = urlopen(req);
	except HTTPError as e:
		print(e);
	except URLError as e:
		print("The server could not be found.")
	else:
		html_text = html.read().decode('utf-8', errors='ignore')
		bs = BeautifulSoup(html_text, 'html.parser');
		posting = bs.find('div', class_ = 'post');
		if posting:
			date = posting.find('div', class_ = 'title');
			calls = posting.find('div', class_ = 'copy');
			listings = CallsListing(str(date), str(calls));
			return listings.get_shortened_calls_all();
		else:
			print("Posting not found");

class CallsListing():
	def __init__(self, date, text):
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
		self.status = re.search(r"(.+?) [cC]all *#", self.full_text).group(1);
		self.schedule = re.search(r"[wW]orking.*?(\d\/\d[^\.]*?)\.", self.full_text).group(1);
