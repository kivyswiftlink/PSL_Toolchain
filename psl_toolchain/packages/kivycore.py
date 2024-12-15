from targets import SwiftTarget
from package import CythonSwiftPackage, SwiftPackage


from kivy_ios.toolchain import Recipe
from kivy_ios.recipes.kivy import KivyRecipe

PackageDependency = SwiftTarget.PackageDependency

class KivyTarget(SwiftTarget):
    
    name = "KivyCore"
    
    recipes = [
        KivyRecipe()
    ]

    dependencies = [
        PackageDependency("SDL2Core", "SDL2Core")
    ]

class KivyCore(CythonSwiftPackage):
    
    include_pythoncore = True
    include_pythonswiftlink = True
    
    products: list[SwiftPackage.Product] = [
        SwiftPackage.Product("KivyCore", ["KivyCore"])
    ]
    
    _targets = [
        KivyTarget(),
    ]
    
    dependencies = [
        SwiftPackage.Dependency("https://github.com/KivySwiftLink/SDL2Core", next_major="311.0.0")
    ]

    site_package_targets = [
        "kivy", "Kivy-2.3.0-py3.11.egg-info"
    ]

package = KivyCore()