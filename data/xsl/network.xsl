<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
  <xsl:output method="text"/>

  <xsl:template match="/">
    <xsl:apply-templates select="/network"/>
  </xsl:template>

  <xsl:template match="network">
    <xsl:text>NETWORKING=</xsl:text>
      <xsl:value-of select="@enabled"/>
    <xsl:text>&#10;</xsl:text>
    <xsl:text>HOSTNAME=</xsl:text>
      <xsl:value-of select="@hostname"/>
  </xsl:template>
</xsl:stylesheet>
