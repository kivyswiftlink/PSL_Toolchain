from recipe import _Recipe
import hashlib
from os.path import join, dirname, realpath, exists, isdir, basename, splitext


class SwiftTarget:
    
    class PackageDependency:
        name: str
        package: str
        
        def __init__(self, name: str, package: str):
            self.name = name
            self.package = package
            
        @property
        def dump(self) -> dict:
            return {
                "name": self.name,
                "package": self.package
            }
    class LinkerSetting:
        kind: str
        name: str
        
        def __init__(self, name: str, kind: str = "framework"):
            self.kind = kind
            self.name = name
            
        @property
        def dump(self) -> dict:
            return {
                "kind": self.kind,
                "name": self.name
            }
            
            
    name: str
    recipes: list[_Recipe]
    dependencies: list[PackageDependency | str ]
    
    @property
    def linker_settings(self) -> list[LinkerSetting]:
        output = []
        for recipe in self.recipes:
            if hasattr(recipe, "pbx_frameworks"):
                for pbx in recipe.pbx_frameworks:
                    output.append(SwiftTarget.LinkerSetting(pbx))
            if hasattr(recipe, "pbx_libraries"):
                for lib in recipe.pbx_libraries:
                    output.append(SwiftTarget.LinkerSetting(lib,"library"))
        
        return output
    
    @property
    def xcframeworks(self) -> list[str]:
        xcs: list[str] = []
        for recipe in self.recipes:
            xcs.extend(recipe.dist_xcframeworks)
        return xcs
    
    def dump_dep(self) -> list[dict | str]:
        deps = []
        for dep in self.dependencies:
            match dep:
                case str():
                    deps.append({
                        "type": "string",
                        "data": dep
                    })
                case _:
                    deps.append({
                        "type": "dependency",
                        "data": dep.dump
                    })
        return deps
                    
        
    
    @property
    def dump(self) -> dict:
        return {
            "type": "target",
            "data": {
                "name": self.name,
                "dependencies": self.dump_dep(),
                "linker_settings": [linker.dump for linker in self.linker_settings]
            }
        }
    
    
class BinaryTarget:
    name: str
    file: str
    github: str
    repo: str
    version: str
    
    _sha256: str
        
    def __init__(self,name: str, file: str, github: str, repo: str, version: str):
        self.name = name
        self.file = file
        self.github = github
        self.repo = repo
        self.version = version
        self._sha256 = None
    
    @property
    def url(self) -> str:
        return f"https://github.com/{self.github}/{self.repo}/releases/download/{self.version}/{basename(self.file)}"
    
    def calculate_checksum(self):
        BUF_SIZE = 65536
        sha256 = hashlib.sha256()
        with open(self.file, "rb") as fp:
            while True:
                data = fp.read(BUF_SIZE)
                if not data:
                    break
                sha256.update(data)
        self._sha256 = sha256.hexdigest()
                
    @property
    def checksum(self) -> str:
        sha = self._sha256
        if sha: return sha
        self.calculate_checksum()
        return self._sha256
    
    @property
    def dump(self) -> dict:
        return {
            "type": "binary",
            "data": {
                "name": self.name,
                "url": self.url,
                "checksum": self.checksum
            }
        }