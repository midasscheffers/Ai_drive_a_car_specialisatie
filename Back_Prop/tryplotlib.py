import matplotlib.pyplot as plt

gen =  [0,1,2,3,4,5,6,7,8,9]



# Two signals with a coherent part at 10Hz and a random part
avr_score = [.1,.2,.3,.5,.7,.7,.8,.8,.8,.9]
best_score = [.2,.3,.5,.7,.7,.8,.9,.9,1,1.1]

fig, ax = plt.subplots()
ax.plot(gen, avr_score, gen, best_score)
ax.set_xlim(0, len(gen)-1)
ax.set_xlabel('gen.')
ax.set_ylabel('avr. fitness & best fitness')
ax.grid(True)



fig.tight_layout()
fig.savefig("graph.png")
plt.show()