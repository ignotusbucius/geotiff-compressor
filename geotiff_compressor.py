#!/usr/bin/env python3

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
from pathlib import Path
import shutil

class GeoTIFFCompressor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        self.selected_files = []
        self.output_directory = None
        self.compression_method = None
        
    def check_gdal_installation(self):
        """Check if GDAL is properly installed and accessible"""
        # First check if gdal_translate is in PATH
        gdal_path = shutil.which("gdal_translate")
        
        if gdal_path:
            try:
                # Test GDAL functionality
                result = subprocess.run(
                    ["gdal_translate", "--version"], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                if result.returncode == 0:
                    return True, f"GDAL found at: {gdal_path}\nVersion: {result.stdout.strip()}"
                else:
                    return False, "GDAL found but not working properly"
            except subprocess.TimeoutExpired:
                return False, "GDAL found but not responding"
            except Exception as e:
                return False, f"GDAL found but error testing: {str(e)}"
        else:
            # GDAL not in PATH - check common installation locations
            common_paths = [
                "C:\\OSGeo4W\\bin\\gdal_translate.exe",
                "C:\\OSGeo4W64\\bin\\gdal_translate.exe",
                "C:\\Program Files\\GDAL\\bin\\gdal_translate.exe",
                "C:\\Program Files (x86)\\GDAL\\bin\\gdal_translate.exe",
                "C:\\GDAL\\bin\\gdal_translate.exe",
                "C:\\tools\\gdal\\bin\\gdal_translate.exe",
                "C:\\ProgramData\\Anaconda3\\Library\\bin\\gdal_translate.exe",
                "C:\\Users\\{}\\Anaconda3\\Library\\bin\\gdal_translate.exe".format(os.getenv('USERNAME', '')),
                "C:\\Users\\{}\\Miniconda3\\Library\\bin\\gdal_translate.exe".format(os.getenv('USERNAME', '')),
            ]
            
            found_installations = []
            for path in common_paths:
                if os.path.exists(path):
                    found_installations.append(os.path.dirname(path))
            
            if found_installations:
                # GDAL is installed but not in PATH
                error_msg = (
                    "GDAL is installed but NOT in your system PATH!\n\n"
                    f"Found GDAL installations at:\n"
                    + "\n".join(f"• {path}" for path in found_installations) + "\n\n"
                    "TO FIX THIS ISSUE:\n\n"
                    "1. Add GDAL to your Windows PATH:\n"
                    "   • Press Win + X, select 'System'\n"
                    "   • Click 'Advanced system settings'\n"
                    "   • Click 'Environment Variables'\n"
                    "   • Select 'Path' in System Variables\n"
                    "   • Click 'Edit' then 'New'\n"
                    "   • Add one of these paths:\n"
                    + "\n".join(f"     {path}" for path in found_installations) + "\n\n"
                    "2. Restart this application\n"
                    "3. Test with: gdal_translate --version\n\n"
                    "ALTERNATIVE: Run Command Prompt as Administrator and use:\n"
                    f'setx PATH "%PATH%;{found_installations[0]}" /M'
                )
                return False, error_msg
            else:
                # GDAL not installed at all
                error_msg = (
                    "GDAL is NOT INSTALLED on your system.\n\n"
                    "INSTALLATION OPTIONS:\n\n"
                    "1. OSGeo4W (Recommended for Windows):\n"
                    "   • Download from: https://trac.osgeo.org/osgeo4w/\n"
                    "   • Run osgeo4w-setup.exe (included in this folder)\n"
                    "   • Install 'gdal' package\n"
                    "   • Installation will add to PATH automatically\n\n"
                    "2. Official GDAL:\n"
                    "   • Download from: https://gdal.org/download.html\n"
                    "   • Choose Windows binaries\n"
                    "   • Manually add to PATH after installation\n\n"
                    "3. Conda/Miniconda:\n"
                    "   • Run: conda install -c conda-forge gdal\n"
                    "   • Should add to PATH automatically\n\n"
                    "After installation:\n"
                    "• Restart this application\n"
                    "• Test with: gdal_translate --version"
                )
                return False, error_msg
        
    def select_files(self):
        """Open Windows Explorer to select GeoTIFF files"""
        while True:
            file_types = [
                ("GeoTIFF files", "*.tif *.tiff"),
                ("All files", "*.*")
            ]
            
            files = filedialog.askopenfilenames(
                title="Select GeoTIFF files to compress",
                filetypes=file_types,
                initialdir=os.getcwd()
            )
            
            if files:
                self.selected_files = list(files)
                # Confirm file selection
                if self.confirm_files():
                    return True
                else:
                    # User said no to confirmation, ask if they want to select different files
                    choice = messagebox.askyesnocancel(
                        "Re-select Files?",
                        "Would you like to select different files?\n\n"
                        "Yes = Select different files\n"
                        "No = Exit application\n"
                        "Cancel = Use current selection anyway"
                    )
                    if choice is True:  # Yes - select different files
                        continue
                    elif choice is False:  # No - exit application
                        return False
                    else:  # Cancel - use current selection
                        return True
            else:
                # User cancelled file selection, ask if they want to exit
                exit_choice = messagebox.askyesno(
                    "Exit Application?",
                    "No files were selected. Do you want to exit the application?"
                )
                if exit_choice:
                    return False
                # If they don't want to exit, continue the loop to select files again
    
    def confirm_files(self):
        """Display selected files and ask for confirmation"""
        if len(self.selected_files) == 1:
            message = f"Selected 1 file:\n{os.path.basename(self.selected_files[0])}"
        else:
            file_names = [os.path.basename(f) for f in self.selected_files]
            message = f"Selected {len(self.selected_files)} files:\n" + "\n".join(file_names)
        
        message += "\n\nAre these the correct files?"
        
        return messagebox.askyesno("Confirm File Selection", message)
    
    def select_compression_method(self):
        """Let user choose between COG and Traditional compression methods"""
        method_choice = messagebox.askyesnocancel(
            "Compression Method Selection",
            "Choose compression method:\n\n"
            "COG (Cloud Optimized GeoTIFF):\n"
            "• Modern format, faster web access\n"
            "• Better for online maps and cloud storage\n"
            "• Requires newer GDAL version\n\n"
            "Traditional TIFF:\n"
            "• Compatible with older GDAL versions\n"
            "• Good for local desktop use\n"
            "• More universal compatibility\n\n"
            "Yes = COG method\n"
            "No = Traditional method\n"
            "Cancel = Abort"
        )
        
        if method_choice is None:  # Cancel
            return False
        elif method_choice:  # Yes - COG method
            self.compression_method = "COG"
            return True
        else:  # No - Traditional method
            self.compression_method = "TRADITIONAL"
            return True
    
    def select_output_directory(self):
        """Ask user to choose output directory"""
        choice = messagebox.askyesnocancel(
            "Output Directory", 
            "Do you want to output files in the same directory? (RECOMMENDED)\n\n"
            "Yes = Same directory\n"
            "No = Choose new directory\n"
            "Cancel = Abort"
        )
        
        if choice is None:  # Cancel
            return False
        elif choice:  # Yes - same directory
            self.output_directory = None  # Will use same directory as input
            return True
        else:  # No - choose new directory
            directory = filedialog.askdirectory(
                title="Select output directory",
                initialdir=os.getcwd()
            )
            if directory:
                self.output_directory = directory
                return True
            return False
    
    def compress_file(self, input_file, output_file):
        """Compress a single GeoTIFF file using GDAL"""
        try:
            if self.compression_method == "COG":
                # COG (Cloud Optimized GeoTIFF) method
                cmd = [
                    "gdal_translate",
                    "-of", "COG",
                    "-co", "COMPRESS=JPEG",
                    "-co", "QUALITY=75",
                    input_file,
                    output_file
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    return False, f"COG compression failed: {result.stderr}"
                else:
                    return True, None
                    
            else:  # Traditional method
                # Traditional TIFF with JPEG compression
                cmd = [
                    "gdal_translate",
                    "-b", "1", "-b", "2", "-b", "3",
                    "-co", "COMPRESS=JPEG",
                    "-co", "JPEG_QUALITY=75",
                    "-co", "PHOTOMETRIC=YCBCR",
                    "-co", "TILED=YES",
                    input_file,
                    output_file
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    return False, f"Traditional compression failed: {result.stderr}"
                else:
                    return True, None
                
        except FileNotFoundError:
            return False, "GDAL not found. Please install GDAL and ensure it's in your PATH."
        except Exception as e:
            return False, str(e)
    
    def process_files(self):
        """Process all selected files"""
        success_count = 0
        error_messages = []
        
        for input_file in self.selected_files:
            # Determine output file path
            input_path = Path(input_file)
            
            if self.output_directory:
                output_path = Path(self.output_directory) / f"compressed-{input_path.name}"
            else:
                output_path = input_path.parent / f"compressed-{input_path.name}"
            
            print(f"Compressing: {input_path.name}")
            print(f"Output: {output_path}")
            
            success, error = self.compress_file(str(input_path), str(output_path))
            
            if success:
                success_count += 1
                # Get file sizes for comparison
                original_size = input_path.stat().st_size
                compressed_size = output_path.stat().st_size
                compression_ratio = (1 - compressed_size / original_size) * 100
                print(f"Success! Compressed by {compression_ratio:.1f}%")
            else:
                error_messages.append(f"{input_path.name}: {error}")
                print(f"Error: {error}")
        
        # Show final results
        message = f"Compression complete!\n\n"
        message += f"Successfully compressed: {success_count}/{len(self.selected_files)} files"
        
        if error_messages:
            message += f"\n\nErrors:\n" + "\n".join(error_messages)
        
        if success_count > 0:
            messagebox.showinfo("Compression Complete", message)
        else:
            messagebox.showerror("Compression Failed", message)
    
    def run(self):
        """Main application flow"""
        print("GeoTIFF Compressor")
        print("==================")
        
        # Step 0: Check GDAL installation
        gdal_ok, gdal_message = self.check_gdal_installation()
        if not gdal_ok:
            print("GDAL Check Failed:")
            print(gdal_message)
            messagebox.showerror("GDAL Installation Required", gdal_message)
            return
        else:
            print(f"GDAL Check Passed:")
            print(gdal_message)
        
        # Step 1: Select files (includes confirmation)
        if not self.select_files():
            print("File selection cancelled. Exiting.")
            return
        
        # Step 2: Choose compression method
        if not self.select_compression_method():
            print("Compression method selection cancelled. Exiting.")
            return
        
        # Step 3: Choose output directory
        if not self.select_output_directory():
            print("Output directory selection cancelled. Exiting.")
            return
        
        # Step 4: Process files
        self.process_files()
        
        print("Done!")

def main():
    """Entry point"""
    try:
        compressor = GeoTIFFCompressor()
        compressor.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

if __name__ == "__main__":
    main()