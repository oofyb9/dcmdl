import os

def main(args):
    plugin_name = args.plugin
    plugin_args = args.args
    plugin_file = f"plugins/{plugin_name}.py"
    if os.path.isfile(plugin_file):
        try:
            spec = __import__(f"plugins.{plugin_name}", fromlist=['main'])
            spec.main(plugin_args)
        except Exception as e:
            print(f"Error executing plugin '{plugin_name}': {e}")
    else:
        print(f"Plugin '{plugin_name}' not found in plugins directory.")