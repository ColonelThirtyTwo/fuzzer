
PAGENAMES = [
	"admin",
	"administrator",
	"admin/index",
	"administrator/index",
]

EXTENSIONS = [
	"",
	".html",
	".htm",
	".php",
	".jsp",
	".asp",
	".aspx",
]

def iter():
	for n in PAGENAMES:
		for ex in EXTENSIONS:
			yield n + ex
