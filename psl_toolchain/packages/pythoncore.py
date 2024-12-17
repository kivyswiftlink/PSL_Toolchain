from psl_toolchain.targets import SwiftTarget
from psl_toolchain.package import SwiftPackage, CythonSwiftPackage

from kivy_ios.toolchain import Recipe
from kivy_ios.recipes import python3, openssl, libffi

PackageDependency = SwiftTarget.PackageDependency

class PythonCoreTarget(SwiftTarget):
    
    name = "PythonCore"
    
    dependencies = ["PythonLibrary"]
    
    recipes = [
        python3.recipe,
        openssl.recipe,
        libffi.recipe
    ]

class PythonLibrary(SwiftTarget):
    
    name = "PythonLibrary"
    
    resources = [SwiftTarget.Resource("lib")]
    
class PythonExtra(SwiftTarget):
    
    name = "PythonExtra"
    
    dependencies = ["libpython3.11"]
    
    
########################################################################################

class PythonCore(SwiftPackage):
    
    repo_url = "https://github.com/kivyswiftlink/PythonCore"
    #include_pythonswiftlink = True
    
    products = [
        SwiftPackage.Product("PythonCore", ["PythonCore"]),
    ]
    
    targets = [
        PythonCoreTarget(),
        PythonExtra(),
        PythonLibrary()
    ]
    
    



package = PythonCore()