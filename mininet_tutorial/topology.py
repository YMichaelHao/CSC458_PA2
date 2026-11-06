from mininet.topo import Topo
from mininet.link import TCLink

class TutorialTopology( Topo ):

  constrained = False
  def build( self ):

    
    # add a switch to the network
    s1 = self.addSwitch( 's1' )
    s2 = self.addSwitch( 's2' )
    n = 5
    for i in range(1, 2 * n + 1):
      if i <= n:
        switch = s1
      else:
        switch = s2
      host = self.addHost( f'h{i}' )
      # add a link between the host `h1` and the `s1` switch
      self.addLink( host, switch )
    if self.constrained:
      self.addLink( s1, s2, cls=TCLink, bw=50, delay='30ms', loss=10 )
    else:
      self.addLink( s1, s2 )

class ConstrainedTopology(TutorialTopology):

  constrained = True

# the topologies accessible to the mn tool's `--topo` flag
# note: if using the Dockerfile, this must be the same as in the Dockerfile
topos = { 
  'tutorialTopology': ( lambda: TutorialTopology() ),
  'constrainedTopology': (lambda: ConstrainedTopology()),
  }
