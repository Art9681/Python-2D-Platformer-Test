import pyglet
from cocos.director import director
import scenes

def main():
    pyglet.font.add_directory('.')
    director.init(width=640, height=480, do_not_scale=True, caption = "Art's 2D Game")
    director.show_FPS = True
    my_scene = scenes.MyGame()

    # run the scene
    director.run(my_scene)

if __name__ == '__main__':
    #Look for resources in the data directory.  If you modify the path, you must call reindex.
    pyglet.resource.path.append('data')
    pyglet.resource.reindex()
    main()