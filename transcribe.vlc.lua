-- VLC Lua extension file that prompts the user for a target language
function descriptor()
    return {
        title = "Transcribe, Remove Voice & Dub",
        version = "1.0",
        author = "Your Name",
        capabilities = {"input-listener", "menu"}
    }
end

local dlg = nil

function activate()
    vlc.msg.info("Transcribe, Remove Voice & Dub extension activated.")
    local item = vlc.input.item()
    if item then
        local uri = item:uri()
        local path = vlc.strings.decode_uri(uri):gsub("^file://", "")
        -- check if transcription file exists
        local srt_path = path:gsub("%.%w+$", "_transcription.srt")
        local f = io.open(srt_path, "r")
        if f then
            vlc.msg.info("Subtitles already exist for this file.")
            f:close()
        else
            show_language_prompt(path)
        end
    else
        vlc.msg.err("No media item loaded!")
    end
end

function deactivate()
    if dlg then dlg:delete() end
end

function meta_changed() end

-- Function to display a simple dialog for language input
function show_language_prompt(video_path)
    dlg = vlc.dialog("Dubbing Settings")
    dlg:add_label("Enter target language code (e.g., en, fr, de):", 1, 1, 1, 1)
    local lang_input = dlg:add_text_input("", 2, 1, 2, 1)
    dlg:add_button("OK", function() 
        local target_lang = lang_input:get_text()
        if target_lang == "" then
            target_lang = "en" -- default to English if nothing entered
        end
        dlg:delete()
        local cmd = string.format('python3 "/path/to/main.py" "%s" "%s"', video_path, target_lang)
        vlc.msg.info("Executing command: " .. cmd)
        os.execute(cmd)
    end, 1, 2, 1, 1)
end