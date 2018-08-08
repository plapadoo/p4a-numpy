import os
from pythonforandroid.recipe import CompiledComponentsPythonRecipe
from pythonforandroid.toolchain import warning


class NumpyRecipe(CompiledComponentsPythonRecipe):
    
    version = '1.14.5'
    url = 'https://pypi.python.org/packages/source/n/numpy/numpy-{version}.zip'
    site_packages_name= 'numpy'

    depends = [('python2', 'python3crystax')]

    recipe_dir = os.path.dirname(os.path.realpath(__file__))

    patches = [os.path.join(recipe_dir, 'patches', 'fix-numpy.patch'),
               os.path.join(recipe_dir, 'patches', 'prevent_libs_check.patch'),
               os.path.join(recipe_dir, 'patches', 'ar.patch'),
               os.path.join(recipe_dir, 'patches', 'lib.patch')
    ]

    def get_recipe_env(self, arch):
        """ looks like numpy has no proper -L flags. Code copied and adapted from 
            https://github.com/frmdstryr/p4a-numpy/
        """

        env = super(NumpyRecipe, self).get_recipe_env(arch)

        py_ver = '3.6'
        if {'python2crystax', 'python2'} & set(self.ctx.recipe_build_order):
            py_ver = '2.7'

        py_so = '2.7' if py_ver == '2.7' else '3.6m'

        api_ver = self.ctx.android_api

        platform = 'arm' if 'arm' in arch.arch else arch.arch

        flags = " -L{ctx.ndk_dir}/platforms/android-{api_ver}/arch-{platform}/usr/lib/" \
                " --sysroot={ctx.ndk_dir}/platforms/android-{api_ver}/arch-{platform}" \
            .format(ctx=self.ctx, arch=arch, platform=platform, api_ver=api_ver)

        if {'python3crystax'}:
            flags += " -I{ctx.ndk_dir}/sources/crystax/include/" \
                     " -I{ctx.ndk_dir}/sources/python/{py_ver}/include/python/" \
                     " -L{ctx.ndk_dir}/sources/crystax/libs/{arch.arch}/" \
                     " -L{ctx.ndk_dir}/sources/python/{py_ver}/libs/{arch.arch}/ -lpython{py_so}" \
                .format(ctx=self.ctx, arch=arch, py_so=py_so, py_ver=py_ver)

        if flags not in env['CC']:
            env['CC'] += flags
        if flags not in env['LD']:
            env['LD'] += flags + ' -shared'

        return env

    def prebuild_arch(self, arch):
        super(NumpyRecipe, self).prebuild_arch(arch)

        warning('Numpy is built assuming the archiver name is '
                'arm-linux-androideabi-ar, which may not always be true!')

recipe = NumpyRecipe()
