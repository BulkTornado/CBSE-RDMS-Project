import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow( QMainWindow ):
	def __init__(self):
		super().__init__()
		self.setWindowTitle( "CBSE Database Manager" )
		self.setGeometry( 600, 300, 700, 400 )
		self.setWindowIcon( QIcon( "icon.png" ) )


def main() -> None:
	app = QApplication( sys.argv )
	
	# Declaring the window GUI
	window = MainWindow()
	window.show()
	
	# Keeping GUI open and
	# handling the closing
	sys.exit( app.exec_() )


if __name__ == "__main__":
	print( f"Currently running {__file__.split( '\\' )[-1]} script" )
	main()
