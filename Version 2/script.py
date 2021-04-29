from collectionBuilder import collection
from windowBuilder import window

c = collection.read('test.pkl')
# # print(c)

# c = collection()
# #Jarvis
# c.addYoutubeItem("https://www.youtube.com/channel/UCoLUji8TYrgDy74_iiazvYA")
# #Danny
# c.addYoutubeItem("https://www.youtube.com/channel/UCSUf5_EPEfl4zlBKZHkZdmw")
# #Drew
# c.addYoutubeItem("https://www.youtube.com/channel/UCTSRIY3GLFYIpkR2QwyeklA")
# #Wilbur
# c.addYoutubeItem("https://www.youtube.com/channel/UC1n_PfsVqxllCcnMPlxBIjw")
# #Tommy
# c.addYoutubeItem("https://www.youtube.com/channel/UC5p_l5ZeB_wGjO_yDXwiqvw")
# #Schlatt
# c.addYoutubeItem("https://www.youtube.com/channel/UC2mP7il3YV7TxM_3m6U0bwA")
print(c.getLength())

w = window()
w.grid(c,7,5)

w.run()