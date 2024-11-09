import edge_tts

async def generate_audio(text,outputFilename):
    communicate = edge_tts.Communicate(text,"fr-FR-HenriNeural")
    await communicate.save(outputFilename)





