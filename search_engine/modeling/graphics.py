from search_engine.index.api import IndexManager
import search_engine.modeling.lib as lib
import matplotlib.pyplot as plt

margin = 1

#needs DataStorage running
def TestCrawler():
    index = IndexManager.get_proxy()
    dimension = [20, 10, 2]
    x, y = lib.split(lib.get_pages(dimension))
    crawler_x, crawler_y = lib.split(index.get_depth_stat())    
    plt.title('crawler verification, dimensions: %s' % dimension)
    plt.plot(x, y, 'b')
    plt.plot(crawler_x, crawler_y, 'ro')
    plt.xlabel('depth')
    plt.ylabel('crawl frontier')    
    plt.show()

def WebSpaceShapes(log_scale = False):
    depth = 80
    dimensions =[[80, 80, 80],[40, 40, 120], [40, 10, 120]]
    for d in dimensions:
        x, y = lib.split(lib.get_pages(d, depth))
        plt.plot(x, y)
    plt.title('different shapes of web space')
    plt.legend(dimensions)
    plt.xlabel('depth')
    plt.ylabel('crawl frontier')
    if log_scale:
        plt.xscale('log')
        plt.yscale('log')
        plt.axis([1, 1000, 10, 10000])
        
    plt.show()  

def DimensionsRecognition():
    dimension = [50, 300, 500]
    depth = max(dimension)/2 + 10
    plt.title('dimensions recognition, dimensions: %s' % dimension)
    x, y = lib.split(lib.dimensions(lib.get_pages(dimension, depth)))    
    plt.plot(x, y, 'b')
    for d in dimension:
        dx = [0.5*d, 0.5*d]
        dy = [0, len(dimension)]
        plt.plot(dx, dy, 'r')
    plt.legend(['dimension recognition', 'dimension values'])
    plt.xlabel('depth')
    plt.ylabel('dimension')
    plt.axis([0, depth, 0, len(dimension)+ 0.2])
    plt.show()

#needs DataStorage running
def WebDimension():
    index = IndexManager.get_proxy()
    x, y = lib.split(lib.dimensions(index.get_depth_stat()))    
    plt.title('web dimensions')
    plt.plot(x, y, 'b', x, y , 'bo')
    plt.xlabel('depth')
    plt.ylabel('dimension')
    plt.show()

if __name__ == '__main__':
    TestCrawler()
    WebSpaceShapes(False)
    WebSpaceShapes(True)
    DimensionsRecognition()
    WebDimension()
