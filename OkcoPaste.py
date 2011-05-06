import sublime, sublime_plugin
import httplib, urllib, json

domain = 'pastoo.dev'
token = '0'*40

def paste(data, domain, token):
	conn = httplib.HTTPConnection(domain)
	url = '/paste/api/create/{0}'.format(token)
	post_data = urllib.urlencode({'paste': data})
	conn.request("POST", url, post_data)
	response = conn.getresponse()

	ret = json.loads(response.read())

	if ret['success']:
		return ret['user'], 'http://{0}{1}'.format(domain, ret['url'])
	return False, False

class OkcoPasteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		data = '\n'.join(self.view.substr(x) for x in self.view.sel() if not x.empty())
		
		user, url = paste(data, domain, token)
		if user is not False:
			self.view.set_status('okco_paste', '{0}: {1} line(s) pasted to {2}'.format(
				user, len(data.splitlines()), url
			))
		else:
			self.view.set_status('okco_paste', 'Failure: Paste failed. Check auth token')

