## Yu Yu Hakusho - Bakutou Ankoku Bujutsukai (J).nes graphics decompressor/compressor
## release by koda 0.1

import argparse
import os

def decompressGraphics(data, code):
    decompressed_data = bytearray()
    i = 0
    while i < len(data):
        byte = data[i]
        i += 1
        if byte == code:
            repeat_value = data[i] 
            repeat_count = data[i + 1]  
            decompressed_data.extend([repeat_value] * repeat_count)
            i += 2  
        else:
            
            decompressed_data.append(byte)

    return bytes(decompressed_data)

def compressGraphics(data, code):
    compressed_data = bytearray()
    i = 0
    while i < len(data):
        byte = data[i]
        count = 1    
        while i + count < len(data) and data[i + count] == byte:
            count += 1
        if count > 2 and count <= 255:
            compressed_data.append(code)  
            compressed_data.append(byte)  
            compressed_data.append(count) 
            i += count

        elif count > 255:
            while count > 255:
                compressed_data.append(code)  
                compressed_data.append(byte)  
                compressed_data.append(255)   
                count -= 255
                i += 255
            if count > 0:
                compressed_data.append(code)
                compressed_data.append(byte) 
                compressed_data.append(count)
                i += count
        else:  
            compressed_data.extend([byte] * count)  
            i += count
              
    return bytes(compressed_data)

def read_rom(rom_file, addr, size):
    with open(rom_file, 'rb') as f:
        f.seek(addr)
        data = f.read(size)
        return data

def export_graphics(out_file, data):
    with open(out_file, 'wb') as f:
        f.write(data)
        print(f"Decompressed {len(data)} bytes at file {out_file}.")

def import_graphics(file):
    with open(file, "rb") as f:
        data = f.read()
    return data

def write_rom(rom_file, data, addr, bank_size):
    if len(data) > bank_size:
        excess = len(compressed_data) - bank_size
        print(f"Error: {excess} bytes exceed bank size.")
        exit()
    else:
        free_space = bank_size - len(data)
        with open(rom_file, "r+b") as f:
            f.seek(addr)
            f.write(data)
            print(f"compressed {len(data)} bytes at file {rom_file}.")
            print(f"Free space: {free_space} bytes.")

def main():
    # Args.
    rom_file = "Yu Yu Hakusho - Bakutou Ankoku Bujutsukai (J).nes"
    
    #Fonts
    out_file_fonts = "DecompressFonts.bin"
    fonts_bank_addr = 0x0042
    fonts_bank_size = 0x2A7
    #Main menu Options
    out_file_mmoptions = "DecompressMainMenuOptions.bin"
    mmoptions_bank_addr = 0xB811
    mmoptions_bank_size = 0x3B4
    #Main menu Title
    out_file_mmtitle = "DecompressMainMenuTitle.bin"
    mmtitle_bank_addr = 0x17591
    mmtitle_bank_size = 0x8C3
    #Mode Select
    out_file_mselect = "DecompressModeSelect.bin"
    mselect_bank_addr = 0x9A96
    mselect_bank_size = 0xD67
    #Koenma's Menu
    out_file_kjmenu = "DecompressKJMenu.bin"
    kjmenu_bank_addr = 0x3145C 
    kjmenu_bank_size = 0x1C0
    #HUD
    out_file_hud = "DecompressHud.bin"
    hud_bank_addr = 0x5A58
    hud_bank_size = 0x26E
    #FIGHT HUD (NOT COMPRESS)
    out_file_fight = "DecompressFIGHT.bin"
    fight_bank_addr = 0x68AC
    fight_bank_size = 0xE0
    
    # Usage
    parser = argparse.ArgumentParser(description="Compressor/Decompressor - YU YU HAKUSHO Bakutou Ankoku Bujutsukai")
    parser.add_argument('-d', '--decompress', action='store_true', help='Decompress data')
    parser.add_argument('-c', '--compress', action='store_true', help='Compress data')

    # Parse arguments
    args = parser.parse_args()

    if args.decompress:
        # Get graphics bank
        compressed_data_fonts = read_rom(rom_file, fonts_bank_addr, fonts_bank_size)
        compressed_data_mmoptions = read_rom(rom_file, mmoptions_bank_addr, mmoptions_bank_size)
        compressed_data_mmtitle = read_rom(rom_file, mmtitle_bank_addr, mmtitle_bank_size)
        compressed_data_mselect = read_rom(rom_file, mselect_bank_addr, mselect_bank_size)
        compressed_data_kjmenu = read_rom(rom_file, kjmenu_bank_addr, kjmenu_bank_size)
        compressed_data_hud = read_rom(rom_file, hud_bank_addr, hud_bank_size)
        compressed_data_fight = read_rom(rom_file, fight_bank_addr, fight_bank_size)
        
        # Decompress graphics
        decompressed_data_fonts = decompressGraphics(compressed_data_fonts, 0x03)
        decompressed_data_mmoptions = decompressGraphics(compressed_data_mmoptions, 0x0D)
        decompressed_data_mmtitle = decompressGraphics(compressed_data_mmtitle, 0x0A)
        decompressed_data_mselect = decompressGraphics(compressed_data_mselect, 0x2A)
        decompressed_data_kjmenu = decompressGraphics(compressed_data_kjmenu, 0x0B)
        decompressed_data_hud = decompressGraphics(compressed_data_hud, 0x03)

        # Export Graphics
        decompressed_graphics_fonts = export_graphics(out_file_fonts, decompressed_data_fonts)
        decompressed_graphics_mmoptions = export_graphics(out_file_mmoptions, decompressed_data_mmoptions)
        decompressed_graphics_mmtitle = export_graphics(out_file_mmtitle, decompressed_data_mmtitle)
        decompressed_graphics_mselect = export_graphics(out_file_mselect, decompressed_data_mselect)
        decompressed_graphics_kjmenu = export_graphics(out_file_kjmenu, decompressed_data_kjmenu)
        decompressed_graphics_hud = export_graphics(out_file_hud, decompressed_data_hud)
        decompressed_graphics_fight = export_graphics(out_file_fight, compressed_data_fight)
        
    elif args.compress:
        # get exported graphics
        decompressed_graphics_fonts = import_graphics(out_file_fonts)
        decompressed_graphics_mmoptions = import_graphics(out_file_mmoptions)
        decompressed_graphics_mmtitle = import_graphics(out_file_mmtitle)
        decompressed_graphics_mselect = import_graphics(out_file_mselect)
        decompressed_graphics_kjmenu = import_graphics(out_file_kjmenu)
        decompressed_graphics_hud = import_graphics(out_file_hud)
        decompressed_graphics_fight = import_graphics(out_file_fight)       

        # Compress Graphics
        compressed_graphics_fonts = compressGraphics(decompressed_graphics_fonts, 0x03)
        compressed_graphics_mmoptions = compressGraphics(decompressed_graphics_mmoptions, 0x0D)
        compressed_graphics_mmtitle = compressGraphics(decompressed_graphics_mmtitle, 0x0A)
        compressed_graphics_mselect = compressGraphics(decompressed_graphics_mselect, 0x2A)
        compressed_graphics_kjmenu = compressGraphics(decompressed_graphics_kjmenu, 0x0B)
        compressed_graphics_hud = compressGraphics(decompressed_graphics_hud, 0x03)
        
        # Write ROM
        write_data_fonts = write_rom(rom_file, compressed_graphics_fonts, fonts_bank_addr, fonts_bank_size)
        write_data_mmoptions = write_rom(rom_file, compressed_graphics_mmoptions, mmoptions_bank_addr, mmoptions_bank_size)
        write_data_mmtitle = write_rom(rom_file, compressed_graphics_mmtitle, mmtitle_bank_addr, mmtitle_bank_size)
        write_data_mselect = write_rom(rom_file, compressed_graphics_mselect, mselect_bank_addr, mselect_bank_size)
        write_data_kjmenu = write_rom(rom_file, compressed_graphics_kjmenu, kjmenu_bank_addr, kjmenu_bank_size)
        write_data_hud = write_rom(rom_file, compressed_graphics_hud, hud_bank_addr, hud_bank_size)
        write_data_fight = write_rom(rom_file, decompressed_graphics_fight, fight_bank_addr, fight_bank_size)
    else:
        print("USAGE: -d  --decompress")
        print("       -c  --compress")

if __name__ == "__main__":
    main()
